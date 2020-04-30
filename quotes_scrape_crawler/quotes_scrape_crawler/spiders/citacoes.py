# -*- coding: utf-8 -*-
import scrapy

class CitacoesSpider(scrapy.Spider):
    
    name = 'citacoes'                                       
    start_urls = [                                          
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for citacao in response.css('div.quote'):                       
            yield {
                'texto': citacao.css('span.text::text').get(),
                'autor': citacao.css('small.author::text').get(),
                'sobre': citacao.css('span a::attr(href)').get(),
                'tags': citacao.css('div.tags a.tag::text').getall(),   
            }

        proxima_pagina = response.css('li.next a::attr(href)').get()        # Pega o link da próxima página no paginador no final da página web

        if proxima_pagina is not None:                                      # Se o link não for nulo (vazio), ou seja, se existir uma nova página
            proxima_pagina = response.urljoin(proxima_pagina)               # obtém o link da próxima página e combina com o endereço atual da URL
            yield scrapy.Request(proxima_pagina, callback=self.parse)       # Chama recursivamente a função parse() para visitar a nova página e coletar dados
