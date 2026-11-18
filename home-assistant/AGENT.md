# 🏠 Agente HA — Auditor & Designer do Home Assistant

> Documento vivo. Edite livremente: adicione dispositivos, regras, preferências visuais e
> lições aprendidas. O agente lê este arquivo antes de cada execução.

---

## 1. Missão
1. **Validar** — encontrar entidades quebradas, integrações com erro, templates inválidos, duplicidades, IPs antigos.
2. **Verificar** — confirmar com dados ao vivo (estado, logs, histórico) antes de afirmar qualquer coisa.
3. **Informar** — gerar um relatório datado em `relatorios/AAAA-MM-DD_auditoria.md` (🔴 crítico · 🟠 atenção · 🟡 manutenção).
4. **Melhorar visualmente** — propor YAML de cards por dashboard seguindo o *Guia Visual* (seção 6).
5. **Corrigir** — entregar YAML pronto para colar; só executar ações no HA que sejam seguras (seção 4).

## 2. Como rodar
**No Claude Code (com o MCP do HA conectado):**
```
Use o agente ha-auditor e faça a auditoria completa
Use o agente ha-auditor só para as TVs
Use o agente ha-auditor e redesenhe o dashboard "Sala" (colei o YAML abaixo)
```
Definição do agente: `.claude/agents/ha-auditor.md`.

**Limitação atual:** o MCP do HA **não lê** os YAMLs dos dashboards nem `/config`. Para revisar um dashboard,
cole o YAML (Dashboard → ⋮ → Editar → ⋮ → Editor de configuração bruta) ou ative o add-on Studio Code Server
e cole os arquivos. 👉 *Ideia de melhoria:* versionar `/config` num repositório git para o agente ler direto.

## 3. Checklist de auditoria (ordem de execução)
1. `get_system_info` — versões, fuso.
2. `get_config_entries(status=error)` e `not_loaded` — integrações quebradas/ignoradas/desativadas.
3. `system_log__get_entries(limit=50)` — agrupar por integração, contar repetições.
4. Template de saúde (seção 7) — unavailable/unknown por domínio, baterias, updates, entidades sem área.
5. **TVs** — comparar estado das 3 integrações de cada TV (seção 5). Se uma diz `off` e outra `on`, suspeitar de IP.
6. Para erros de template: procurar `entity_id` inexistente (`states('x')` de entidade que não existe).
7. Gerar relatório + YAMLs corrigidos.

## 4. Regras de segurança
- ✅ Pode sem perguntar: ler estados/logs/histórico, renderizar templates, recarregar config entry, `logger.set_level` (voltar para `warning` no fim).
- ⚠️ Perguntar antes: ligar/desligar dispositivos, abrir apps na TV, mexer em fechadura/portão/alarme, `homeassistant.restart`.
- ❌ Nunca: remover integrações, apagar entidades, alterar automações sem o YAML aprovado.

## 5. Inventário — TVs Samsung
| TV | Oficial `samsungtv` (usar p/ comandos) | SmartThings (usar p/ ligar e volume) | Custom `samsungtv_smart` (legado) | IP fixo |
|---|---|---|---|---|
| 70" Sala (UN70U8500) | `media_player.sala_70_sala` / `remote.sala_70_sala` | `media_player.sala_de_estar_70_sala` | `media_player.sala_70_sala_2` (IP antigo .7) | **192.168.68.15** ← reservar no Deco |
| 75" Sala de TV (UN75U8100) | `media_player.75_crystal_uhd_un75u8100fgxzd` | `media_player.sala_de_tv_sala_de_tv_75` | `media_player.media_player_sala_de_tv_sala_de_tv_75` (.17) | ? (.13) |
| Quarto Be (UN49NU7100) | — (não configurada) | `media_player.quarto_quarto_be` | `media_player.media_player_quarto_quarto_be` (.22) | ? |
| QLED Master (QN65Q65D) | ignorada ⚠️ | `media_player.qled_master` | desativada | ? |

### Abrir apps (Tizen)
`media_player.play_media` na entidade **oficial** com `media_content_type: app`:

| App | ID | Validado? |
|---|---|---|
| Netflix | **11101200001** | ☑ 18/11 na 70" (`3201907018807` abre o Samsung TV Plus — não usar) |
| YouTube | 111299001912 | ☐ |
| Prime Video | 3201910019365 | ☐ |
| Disney+ | 3201901017640 | ☐ |
| Max (HBO) | 3202301029760 | ☐ |
| Globoplay | 3201908019041 | ☐ |
| Spotify | 3201606009684 | ☐ |

**Validar App IDs:** num navegador na rede de casa abra `http://192.168.68.15:8001/api/v2/applications/<ID>`.
Retornou JSON com `"name"` → ID certo (marque ☑). Retornou 404 → ID errado para esse modelo; procure o correto
e atualize aqui **e** em `scripts/tv_streaming.yaml`.

## 6. Guia Visual (preferências)
> Ajuste à vontade — o agente segue isto ao redesenhar cards.
- Cards base: **Mushroom** (+ card-mod para efeitos). Controle de TV: **Universal Remote Card**.
- Cantos 14–22 px, fundo sutil `rgba(255,255,255,.04)`, sem bordas fortes.
- Cores semânticas: verde = ligado/carregando, vermelho = crítico/≤20 %, cinza = normal/desligado, laranja = atenção.
- Ícones de apps com a cor da marca.
- Sempre `| int(0)` / `| float(0)` e tratar `unknown`/`unavailable` com texto amigável ("Sem leitura").
- Um dashboard por área; topo com "chips" de status (pessoas, clima, alarmes, baterias baixas).
- Esconder entidades `unavailable` com `visibility`/conditional em vez de mostrar card quebrado.

## 7. Template de saúde (colar em Ferramentas de Desenvolvedor → Modelo)
```jinja
Indisponíveis: {{ states | selectattr('state','eq','unavailable') | list | count }}
{% for d in states | selectattr('state','eq','unavailable') | map(attribute='domain') | unique %}
- {{ d }}: {{ states[d] | selectattr('state','eq','unavailable') | list | count }}{% endfor %}
Baterias < 25%: {% for s in states.sensor | selectattr('attributes.device_class','defined')
  | selectattr('attributes.device_class','eq','battery') %}{% if s.state | int(100) < 25 %}{{ s.name }} ({{ s.state }}%) {% endif %}{% endfor %}
Updates: {{ states.update | selectattr('state','eq','on') | map(attribute='name') | join(', ') }}
```

## 8. Histórico de problemas & soluções (adicione novos no topo)
| Data | Problema | Causa | Solução | Status |
|---|---|---|---|---|
| 2026-11-18 | Netflix abria o Samsung TV Plus | App ID novo `3201907018807` não vale para a UN70U8500 | Usar ID antigo `11101200001`; esperar ~10 s após ligar antes de abrir o app | ✅ testado |
| 2026-11-18 | Botões de streaming do controle da TV não funcionam | `samsungtv_smart` com IP antigo (70": .7 → .15); entidades presas em `off` | Script `tv_streaming.yaml` usando integração oficial + reserva DHCP | ⏳ aplicar |
| 2026-11-18 | Card bateria Mello Tool com erro de template | `mello_tools_*` vs `mello_tool_*` | `card_bateria_mello_tool.yaml` | ⏳ aplicar |

## 9. Roadmap do agente (ideias)
- [ ] Versionar `/config` no git (add-on *Git pull* ou Studio Code Server) → agente lê dashboards direto.
- [ ] Reserva DHCP para todos os dispositivos de rede (TVs, Echos, Tuya).
- [ ] Automação: notificar quando bateria < 20 % ou entidade crítica `unavailable` > 1 h.
- [ ] Atribuir área às 101 entidades sem área.
- [ ] Limpar teamtracker antigos e excluir `sensor.tabela_*` do recorder.
- [ ] Rodar auditoria semanal agendada (ex.: segunda 08:10).
- [ ] Remover `samsungtv_smart` depois de 2 semanas com o controle novo estável.

## 10. Notas livres
_(escreva aqui preferências, dispositivos novos, coisas que o agente deve lembrar)_
