# Pyke - Robô Submarino - TCC ROBÔS

## Integrates: 

Franscisco Ribeiro Silva Lima
Henrique Luisi Fernandes Pinto
Igor Croce Holanda

# Descrição

Pyke é um robô subaquático que implementa ROS2 para realizar leitura de sensores, movimentação e controle.
Dispõe de 3 pacotes principais:

## Sensor_node
    Responsável por publicação da mensagem dos seus diferentes sensores

## Ucracks_node
    Responsável por realizar a obtenção de imagem e tratamento das mesmas a partir de um modelo de segmentação U-net;
    utiliza a câmera integrada na Raspberri Pi 4 para obter imagens e tratá-las. Capturas são realizadas a cada 3 segundos.
    Imagens obtidas durante o processo de captura são guardadas até que a próxima seja capturada; nessa instância, node realizará a comparação das duas imagens, buscando o overlap entre ambas com a implementação do OpenCV.
    Publica máscara para visualização do usuário e porcentagem de chances de haver uma falha estrutural na região analisada 

## Controller_node
    Responsável pelo controle da movimentação do robô; 
    Se inscreve nos nodes de sensores e máscara/chance de falha estrutural, utilizando essas informações para informar o usuário sobre o que o robô está vendo.