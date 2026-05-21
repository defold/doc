---
title: Otimizando o uso de bateria de um jogo Defold
brief: Este manual descreve como otimizar o uso de bateria de um jogo Defold.
---

# Otimizando o uso de bateria
O uso de bateria é uma preocupação principalmente se você tem como alvo dispositivos móveis/portáteis. Uso alto de CPU ou GPU drenará rapidamente a bateria e superaquecerá o dispositivo.

Consulte os manuais sobre como [otimizar o desempenho em tempo de execução](/manuals/optimization-speed) de um jogo para aprender como reduzir o uso de CPU e GPU.

## Desabilitar o acelerômetro
Se você está criando um jogo mobile que não usa o acelerômetro do dispositivo, é recomendado [desabilitá-lo em *game.project*](/manuals/project-settings/#use-accelerometer) para reduzir o número de eventos de entrada gerados.

# Otimizações específicas de plataforma

## Android Device Performance Framework

Android Dynamic Performance Framework é um conjunto de APIs que permite que jogos interajam mais diretamente com os sistemas de energia e temperatura dos dispositivos Android. É possível monitorar o comportamento dinâmico em sistemas Android e otimizar o desempenho do jogo em um nível sustentável que não superaqueça os dispositivos. Use a [extensão Android Dynamic Performance Framework](https://defold.com/extension-adpf/) para monitorar e otimizar o desempenho do seu jogo Defold em dispositivos Android.
