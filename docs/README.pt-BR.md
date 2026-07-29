# Eye Exercise Reminder

[English](../README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Español](README.es.md) · **Português**

**Eye Exercise Reminder** é um aplicativo leve de sobreposição de desktop para Windows,
construído com Python e PyQt6. Ele lembra você periodicamente de fazer exercícios para os
olhos, ajudando a reduzir o cansaço visual em longas sessões de tela.

O lembrete aparece como uma janela flutuante sempre no topo que exibe uma imagem com
instruções de exercícios. É totalmente configurável, suporta 12 idiomas e pode ser iniciado
em modo silencioso, sem janela de console.

## Recursos

| Recurso | Detalhes |
|---|---|
| Intervalo configurável | Lembrete de 1 a 180 minutos |
| Soneca | Adia o lembrete por um número fixo de minutos |
| 12 idiomas | EN, UK, RU, DE, ES, FR, IT, ZH, JA, PL, PT, TR |
| Configurações persistentes | O idioma é salvo localmente em JSON |
| Sempre no topo | A sobreposição fica acima das outras janelas |
| Arrastável | Mova a janela para qualquer lugar da tela |
| Inicialização silenciosa | Execução sem console via `start.pyw` |

## Instalação e execução

Requer Python 3.11+; a única dependência externa é o PyQt6.

```bash
git clone https://github.com/Topicspot/eye-exercise-reminder.git
cd eye-exercise-reminder
pip install PyQt6
python eye_reminder.py    # com saída no console
pythonw start.pyw         # modo silencioso (somente Windows)
```

A imagem de exercícios (por padrão `eye_exercises.png`) deve ficar na mesma pasta que
`eye_reminder.py`.

A documentação completa (configuração, privacidade, solução de problemas) está no
[README em inglês](../README.md).

## Licença

MIT.
