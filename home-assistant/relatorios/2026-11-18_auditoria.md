# Auditoria Home Assistant — 18/11/2026

**Sistema:** HA OS 18.5 · Core 2026.11.1 · Raspberry Pi (aarch64) · 387 entidades · fuso America/Sao_Paulo

## 🔴 Crítico

### 1. Streaming do controle da TV não funciona — CAUSA RAIZ
| TV | Integração `samsungtv_smart` (custom, usada nos botões) | IP real hoje | Estado |
|---|---|---|---|
| 70" Sala | `192.168.68.7` | **`192.168.68.15`** (confirmado pela API da TV) | presa em `off` desde o boot de 16/11 |
| 75" Sala de TV | `192.168.68.17` | `192.168.68.13`? (a oficial tenta este) | presa em `off` |
| Quarto Be | `192.168.68.22` | desconhecido (TV offline no SmartThings desde 05/11) | presa em `off` |

- O roteador (Deco, faixa 192.168.68.x) trocou o IP das TVs via DHCP. A integração **oficial** `samsungtv` se re-descobre sozinha; a **custom** `samsungtv_smart` não.
- Resultado: `media_player.sala_70_sala_2` fica `off` → `select_source: Netflix` é ignorado. Os `remote.*` dessa integração ficam `unknown`.
- Os vínculos SmartThings dessa custom apontam para device IDs `a3cb2b67…` e `1f27372f…`, ambos `OFFLINE` no SmartThings desde 05–09/11.
- Recarregar a integração (feito hoje) **não resolve**: o IP está gravado na config entry.

**Correção (em ordem):**
1. No app Deco: **Reserva de endereço** para cada TV (70" Sala → `192.168.68.15`, MAC Wi-Fi `00:7D:3B:DA:3B:E9`; repetir para 75" e Quarto Be).
2. Usar `scripts/tv_streaming.yaml` + `dashboards/controle_tv_70_sala.yaml` (passam a usar a integração oficial, que já está funcionando).
3. Opcional: em *Configurações → Dispositivos → SamsungTV Smart*, excluir e readicionar cada TV com o IP fixo (aceitar o pop-up "Permitir" na TV).
4. QLED Master: a integração oficial `samsungtv` está **ignorada** e a `samsungtv_smart` **desativada** → não há controle local. Em *Integrações → Ignoradas*, reativar "QLED MASTER".

### 2. Card de bateria "Mello Tool" quebrado
Template usa `sensor.mello_tools_battery_level` (com **s**); entidade real é `sensor.mello_tool_battery_level`. Gera 5 erros de template por render. → `dashboards/card_bateria_mello_tool.yaml`.

## 🟠 Atenção
- **110 entidades `unavailable`**, principais grupos:
  - Interruptores Tuya/Zigbee offline: `int_entrada_*` (6), `8_gang_switch_*` (9), `sala_de_tv_2_*`, `quarto_master_switch_*`, `switch.salatvcentral`, `externo`, `hall`, `garage`, `latexterno`, `arandelas_garagem`.
  - Echos: Cozinha, Master QLED, grupos (Todo lugar, Salacozinha, Hometheater) — e 1504 avisos do `alexa_devices`.
  - Sensores de energia `energy_meter_*`, `contact_sensor_porta` (bateria `unavailable`).
  - Teamtracker antigos (`sensor.palmeiras`, `corinthians_*`, `teste_corinthians_all`) — candidatos a remoção.
- **DNS instável no boot** (MQTT, met.no, Amazon, ESPN falharam por DNS em 16/11). Conferir DNS do HA (*Configurações → Sistema → Rede*), sugerido 1.1.1.1/8.8.8.8 como secundário.
- **Recorder:** `sensor.tabela_*` (4) com atributos >16 KB → excluir do recorder.
- **101 entidades sem área** (light/switch/sensor/media_player) — dificulta dashboards automáticos e Assist.
- **Duplicidade:** cada TV aparece em até 3 integrações (oficial, SmartThings, custom) → 16 `media_player`. Nomes confusos (`media_player.media_player_quarto_quarto_be`, friendly name = entity_id).

## 🟡 Manutenção
- Atualizações: Core 2026.11.2, Universal Remote Card 4.12.6, Mushroom 5.3.0, Alexa Media Player 5.21.0, browser_mod 3.4.2, Config Template Card 2.1.1.
- Baterias: iPad Gabriela **15 %**; Mello Tool 37 %; fechadura Zigbee 67 %.
- Só **1 automação** (`hall_acender_ao_desbloquear_a_porta`, último disparo 30/09).

## Ações feitas pelo agente nesta sessão
- Recarregou `samsungtv_smart:8D3Z` (sem efeito — confirma IP gravado).
- Ligou log debug temporário de `samsungtv_smart`/`samsungtvws` para diagnóstico e **voltou para `warning`**.
- Nenhum comando enviado às TVs.
