from flask import Flask, render_template, request, flash
# from PIL import Image
import base64
import io
import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import urllib

app = Flask(__name__)
app.secret_key = "nosecret"


@app.route("/")
def index():
    flash("Enter the link Here:")
    return render_template("index.html",
    img_data='thisisdeliberatelydonehttps://raw.githubusercontent.com/Mahutrivedi/Flipkart_project/main/smiley.png',
    review_image='https://raw.githubusercontent.com/Mahutrivedi/Flipkart_project/main/stars.jpg')

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())



@app.route("/Sentiment", methods=['POST', 'GET'])
def Linker():
    
    temp=request.form['link_input']
    sep = 'marketplace=FLIPKART'
    URL = temp.split(sep, 1)[0]
    URL=URL.replace('/p/','/product-reviews/')
    URL = URL+sep

    code = requests.get(temp)
    new_soup = BeautifulSoup(code.content,'html.parser')
    Name = new_soup.find_all('span',class_='B_NuCI') 
    Name=str(Name)
    Name=Name.split('>')
    Name=Name[1].split('<')
    Name=Name[0]
    flash("Product Name: " + Name  )

  
    soup = BeautifulSoup(code.content,'html.parser')
    image = soup.find_all('div',class_='CXW8mj _3nMexc')
    image=str(image).replace('1x"/></div>','')
    image= image.replace(']','')
    image=image.split(" ")
    Link=image[-2]

    Mytemp=URL
    new_code = requests.get(Mytemp)
    new_soup = BeautifulSoup(new_code.content,'html.parser')
    stars = new_soup.find_all('div',class_='_1uJVNT')
    five_star = int(stars[0].text.replace(",",""))
    four_star = int(stars[1].text.replace(",",""))
    three_star = int(stars[2].text.replace(",",""))
    two_star = int(stars[3].text.replace(",",""))
    one_star = int(stars[4].text.replace(",",""))
    Positive = five_star + four_star
    Negative = one_star + two_star +three_star
    name = ['Positive Reviews','Negative Reviews']
    result = [Positive,Negative]
    results = pd.DataFrame(columns=name)
    results["Reviews"] = result
    results["Category"] = name
    results["% Count"] = results["Reviews"]*100/(Positive+Negative)
    results["% Count"]=results["% Count"].round(1)

   
    


    plt.legend(fontsize=20)
    fig,ax=plt.subplots(figsize=(6,6))
    ax=sns.set(style="darkgrid")
    sns.barplot(data=results,y="Reviews",x="Category", color='green',palette = ['tab:red', 'tab:green'],hue=results["% Count"])
    
    canvas=FigureCanvas(fig)
    img=io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    return render_template("index.html", img_data=Link,review_image=plot_data)

