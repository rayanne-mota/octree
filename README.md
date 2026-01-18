# octree

Imagine um quarto muito, muito bagunçado, cheio de brinquedos espalhados por todo lado: no chão, em cima da cama e até pendurados no teto.

Se eu te pedisse para achar o seu boneco favorito, você ia demorar um tempão procurando no quarto todo, né?

A Octree é como uma "mágica de organização" para o computador não ter esse problema. Ela funciona assim:

    A Caixa Gigante: Imagine que a gente coloca o quarto inteiro dentro de uma caixa gigante transparente.

    A Regra dos 8: Se essa caixa tiver muitos brinquedos dentro, a gente divide ela em 8 caixas menores (quatro na parte de baixo e quatro na parte de cima).

    Repetindo a Mágica: Se uma dessas caixinhas menores ainda estiver muito cheia de brinquedos, a gente divide ela de novo em mais 8 caixinhas minúsculas.

A gente faz isso até que cada caixinha tenha poucos brinquedos.

Por que isso é legal? Quando você quiser achar seu boneco, você não precisa revirar o quarto todo. O computador vai dizer: "Não precisa olhar na caixa do teto, nem na caixa da janela. Vá direto na caixinha minúscula perto da porta!"
