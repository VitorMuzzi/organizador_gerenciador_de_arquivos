organizador da pasta downloads do Windows. 

separa os arquivos na pasta Downloads em 5 pastas diferentes e cria um arquivo .TXT para logs

    - Compactados
    - Documentos
    - Imagens
    - Instaladores
    - Outros
    - historico_organizacao

no config.json voce pode mudar as configurações do scripts, sendo nescessario trocar o endereço padrão que está lá pelo endereço da sua pasta \Downloads.

Tambem é possivel criar uma nova pasta ou alterar uma já existente, assim como mudar qual extensão é adicionada em qual pasta. 

Os arquivos com extensões não determinadas são levadas pra pasta \Outros

é possivel rodar o codigo com "--auto" para que o codigo rode de 60 em 60 segundos. Mantendo a pasta downloads sempre organizada.

(lembre-se das duas contra-barras (\\) no lugar de apenas uma quando substituir o endereço do Downloads no config.json)