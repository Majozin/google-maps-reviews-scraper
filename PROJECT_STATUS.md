# Status do projeto

`PROJECT_STATUS.json` é a fonte de progresso deste projeto. Todo projeto novo deve nascer com este arquivo; atualize-o no mesmo PR das entregas, respeitando os gates locais.

Campos obrigatórios: schema_version (1), repository (owner/repo), name, publish (booleano), updated_at (YYYY-MM-DD), scope (name e revision inteira positiva), milestones (lista).

Cada marco exige id único, state e weight inteiro de 1 a 1000. Estados: planned, in_progress, in_review, blocked, done, cancelled. done exige evidence com referências verificáveis e os gates de conclusão locais. Títulos e evidências permanecem no repositório de origem.

Progresso = floor(100 × pesos done / pesos não cancelados). Sem marcos ativos: 0%. Bloqueadas e em revisão não recebem crédito parcial. Pesos iguais medem quantidade de entregas, não prazo/esforço. Mudanças de escopo exigem incrementar scope.revision e justificar no PR; não manipular pesos para elevar o percentual.

Valide com `python3 scripts/project_status.py PROJECT_STATUS.json`. O workflow project-status executa esta validação. publish:true autoriza somente nome e agregados no perfil; false exclui o projeto. A coleta só considera a branch integrada configurada no perfil, nunca uma branch de PR.

A auditoria inicial é documental, sem testes funcionais ou garantia de prontidão de produção. Um baseline vazio significa ausência de estimativa, não ausência de implementação.

Modelo e criação de novos projetos: https://github.com/Majozin/Majozin/blob/main/docs/PROJECT_STATUS.md
