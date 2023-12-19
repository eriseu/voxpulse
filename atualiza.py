import requests
import feedparser
from bs4 import BeautifulSoup
from instabot import Bot

# Função para buscar a imagem através do endereço da notícia no WordPress
def get_image_from_wordpress(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    image_element = soup.find('img')
    if image_element:
        image_url = image_element['src']
        return image_url
    return None

# Função para publicar uma imagem no Instagram
def post_to_instagram(image_url, caption):
    bot = Bot()
    bot.login(username='${{ secrets.LOGIN_INSTAGRAM }}', password='${{ secrets.SENHA_INSTAGRAM }}')
    bot.upload_photo(image_url, caption=caption)

# URL do feed RSS
rss_url = 'https://n.centraleti.com.br/feed'

# Faz o parse do feed RSS
feed = feedparser.parse(rss_url)

# Lê as últimas postagens do feed
num_posts = 3  # Número de postagens que você deseja publicar
for i in range(num_posts):
    entry = feed.entries[i]

    # Obtém o título, link e descrição da postagem
    title = entry.title
    link = entry.link
    description = entry.description
    
    # Obtém a imagem do endereço da notícia no WordPress
    image_url = get_image_from_wordpress(link)

    # Verifica se a imagem foi encontrada
    if image_url:
        # Aqui você pode adicionar lógica adicional para processar os dados da postagem
        
        # Exemplo: publica o título, link e imagem no Instagram
        post_to_instagram(image_url=image_url, caption=f'{title}\n{link}')
