GUSTAVO AUAD PICCOLI - 00275858 - Turma: A 
JÚLIA DEL PINO RITTMANN - 00262512 - Turma: A 
NÍKOLAS PADÃO SCHUSTER - 00323741 - Turma: A

A única biblioteca necessária para ser instalada no python3 é a matplotlib

##################################################################################################################
Problema 1:


##################################################################################################################
Problema 2:
Ao meu ver os valores dos thetas que melhor resultam na melhor execução, tem valores próximos de um valor após muitas execuções com um valor qualquer. Assim, escolho os seguites valores após 10000 execuções com thetas iniciais iguais a 0:
theta_0: 3.9999999999999947
theta_1: -0.29999999999999827

Para o valor de alfa, após múltiplos testes chego a conclusão um valor que resulta em uma melhor execução da sua regressão linear é:
alpha = 0.115

Para o valor de num_interations, quanto maior o número, mais aproximado serão os valore de theta_0 e theta_1 dos seus valores ótimos. Mas se eu utilizar já excelentes thetas e alpha, posso reduzir muito o tamanho de num_iterations. Por exemplo se:
theta_0: 3.9999999999999947
theta_1: -0.29999999999999827
alpha = 0.115
Posso atingir um bom resultado com:
num_iterations = 50

Caso eu começo com thetas e alpha piores, um valor razoável é:
num_iterations = 1000

Para o erro quadrático médio, temos que com os thetas originais:
theta_0: 0
theta_1: 0:
erro_quadratico_medio = 11.25

Para o erro quadrático médio, temos que com os thetas melhorados:
theta_0: 3.9999999999999947
theta_1: -0.29999999999999827
erro_quadratico_medio = 0.5750000000000002

Isso mostra que esses novos thetas são muito melhores, pois o erro quadrático médio deles é muito menor do que com os thetas originais.
