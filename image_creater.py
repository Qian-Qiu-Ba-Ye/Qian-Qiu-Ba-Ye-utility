from openai import OpenAI
import os
import json
import requests
import time
import random
from bs4 import BeautifulSoup
from gpt4_openai import GPT4OpenAI

from PIL import Image


ORGPATH=os.path.dirname(os.path.abspath(__file__))
FORWARDED_IP = (
    f"13.{random.randint(104, 107)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
)
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6",
    "cache-control": "max-age=0",
    #"content-type": "application/x-www-form-urlencoded",
    # "referrer": "https://www.bing.com/images/create/",
    # "origin": "https://www.bing.com",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-forwarded-for": FORWARDED_IP,
    "Cookie":'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..O-uXyBV7S6PvSfZe.yYNfq1q8qfDMHzkSwaL0tmhkdmG3qJkxoatWKgg8_moTKP0AhisFWCyPOxqPRkwL73_gPbm-hFat4zZKLLxK8CiGHJ15NCAJQuODiuLo28G18iThI5-jKLPgmZREGeIYOl1SsDCRKpDMBf_nbqj1RjMcc1aDbrC5mscjjtUiXjsnyhrmKNe4b7Dug7tpe39_ImAxMYcH5Xz8skGE4I7eaqCruW2WxZBHHyfqkQ1B5uF3m01aNs_bQyt--5Ygj4VsiAwDTwLOJe4jt33AnI3cYFs3bPzv09YS68ykVf1dYu1KrHyLHXkERxWjBaxodmqIanKVW980lq7JNLZc4NRccCWIGE3JUj_X1TB-xxJw3uzCjpWFIHOsGFr8E3h4XiQiIoLDDYl5CksM-YJ9Cqv3RSXubJ4048H6NYyTyeKqQVzt3_gOP1cVPUCl584oY6XSy5c284YQZXQPRHMeqJxDGM8QuyM19GNeuldFbpj3rmAooKbDhucoV76aaemS0Dm6I37ByOsXgBs1yqOFy_XwIUeVz53XqSdE5goBLb3LFZj8ARqZCGDfysupeODwpsdw6Z_quCiyumadIxWVaWF6ib2jF_-hMGDokmop7F0byNJ4gGEMg8BdF1GTtcoeJJ06mt_fniBwZcT6a2qGD94TggUg4lCIcYDhOewKNZagJPCIPf2j0mEAyw2f2X4LLCoJ6hlSdXVZWGZ6Gu8YC3GSBeUtEk0HykpGcdFaX6CwsvdLE-HfGTu5daMJVBK52XoacHYqbMxgR4b5VVoo4LEJK7hDQLwZjrKeCHxkt8sV8_NY7rFQZCBQltf8l0K3JBVURvnnv0XsOPISJYbxhg-ERf7GFcTYnDPx_Py84OooHGCdFZz6E9paUjEtKx25p07Z65ZpyOueLHuU-pLuXPNBpDLP2YcmWhNENxjZa1WPgMIBhXKoKfZFPLcgxTX5tRn1e7h4u5mZTuaiDj71x7UlT_k-FB3ZLZlEInDa7E8xptBUA7P0sC1TcMPy891hloLCpZB2gLPCidnGUcHbXfCdFlubuz70Z4ErHFKKEESF53u8O9qC6YNwTVS1GdSsjI6Y5cgypf7a4LVzd-K2Ev2AyAb3LenmIjB2hrinStXaFKqfhhfeSgImMgQZ7caopY5IrClVAgYWX5y5GO5ziQFBXzW06IcHUk--t5KU2Sa4ToI4LKmvyc0Q_QRD9Rz8fTt2OfmyAV69S9yVKUh5Xyl0DI3cxkzXJKIBvml3p7QJE4lTLn4x3jLiFJx9oSJLFRXKtk65nK5AtHRAysOZYOFbPT7UafiqaFivT4JZto517Q1iUeLrPAgXnpZ5SlJsapxhFz7LbCVWdHCf6HHjYaGJK8elfKdokKB7fs1fQM72SjUCdUHQTeol05we0jpYRstggvIEhm9lOKfoL2QLfcoXd6xe1_UgnzJ6Qn9maJg2I0x8I6FSkPNGf1f1TIydQgntriGp40JX2cEvGLaGDcqO5wEuU-99D4zmq9IABYenXWVPCVeCjzNBPAmkL-ydODXda_NKtOU_BYORLyc8zKdTnpngsCfrlD0MCEmQQ36ATXZSTqUkpToiz3R2WY4yDqVx9qftqn9k7_s1GJz5iXt6U2nDU5B6J70bMPTUA4sHijRrFxd-04Ld67y8O6R6pRw4DoqpeLcvai28jEqYIzKXZHW7Iq0L9tdB1wRpXoOgjVdLNpd2jip-XnFVM4f2YHfKEPp1Q0G8ysvBoTw_ohD9thbNdYRcK9n2k5whP7Dr4cRudRNiNwyvUDjrJM0w0PEYrcUp-KSpZojJUQbZ021nc3ylvpaj3qykOnhy0HDrfd6deY5zZ2yHNaAL7iF1ZtHPn5HIq4j-GeAXBKrz4I_KMyrzw5z_D3eKfYhscjVn9RYwTlpO2gqxz1vPxonoPoEWg7zrPGuFpLKM263MUbf0lZCLQiykgJmgj66H2VNKEfCukg2Ka200DuAtkXa5crciFmqBohkgIZJfC5oBcqdA3Cc-07byosdGnARevevcamCV9Qrzjnyjs18BkTnPYaxT1Je7Qu4HDBHF3cQEIq7E9U1s8V6yCrNq8MaMohL1sUJ774qMcxawUTtm6OQyFOFnarCPv8rA2rHAMhxHFSufhvBUkkQpq0sxKKpt0URq8UjiFMC2Y7mgPgfld9rPL-vHCaYtl1m7X0m_ovDL5FQB7OfLqj2oMRvAdMIuELY4tIpK7uTMWKBtul5_V8RRFGePYuTh3GY0STNl7-dL_unzQtUkhP2VnvnAwAz76olE4Rmh-p3LGbnE5TfZsnCcRBFGjV1odHU6pW80f3Zrt4L-XVdsZ3rN3M-UkD-0eo0mBmMyCHzD_VCn3TDJsAPyYqR8cGUbHp6As5kKnT2lIEAwxSEgzz3qq8bXul-Ca20a5C90ncxuEMa5QoKtYpieki5YLo706JBTnRUF75qB7-NzqSK2pCJ0XKOcQ5wHN1Njz_Pj2XS-pYgZODI-JjWCNNXrh3vn_5sFE2_9ZJropBudlMBZCurdYVe5j5P7QxQ85Y3ohYIB37gIsEYnrdYyR3MvLwuOlOtgV6yoFZfozrUjojrT-VKgIgUAAFiGq70mF1hRn8otJWK8j4fqONRY2r_IPppdgHyrqo173Lca-wnF8tEPX_9nkr8FtAjliOVn940Ua9PQfgyu3_qoydKJiabZMCf6WNhp8VKj_qJI9beOzGHkJ-gmCsCemJ-rZsKjFz19V-fxBuZQhSA1Hi2DITIsUA-Kc4IdykPf96nAsS1Ugdp1H9TalWjolGMRXYfSR3PzZa3nek-mTlce8WZfIYIM0K5Fpulhy20bmTgd8AUcH0al7Lr7XOf_rg-O35Il0WFKgEJKQSdXT-9qoMjQ_5kE_MLiYhqwddpa11IMiymeh8NTFUrjXBIPkHNK45qPdG7itZvqf64IkoXB6Uw-QeEJUG9SG0KaEjojgDAjv97lC-fsh4PClq5dJmAPUsY_h8sQbAuqD1eqBOcs0xicOWYfjGqMesz3cRe0Nc4egJZRsEHRuI-UN5wsEr8HKlzwvGaKdXvJ6pPw6H0EhHJQYD-ZF-cG0ZC2uw9Nq6QUlKBnVgTCAj4hVNXG3sU2b9sN6sU6cchezIjVwMKLd5Bi0Ylbt7N-DdsLfkf66KhWUw0cDwKLVD_NAKoEGC5QtwyZ9QKjfxDvzVzy4Drx8JL9ISVaegtZapXB_pLjMvnBgtgBvbBPrC6lRIwYRdvA3MHyGCycInbSoaFnL3zwRDkoCr6-SFiMVMdk-eQVXGNlDNG13LOnNeRk8q44Ceyvn3L9eV8UJj0Hh10tBV1d5Qdt9TBNAS7Q-IWHtlJJ_ZYnylBxT4bNd1MizyHLYrYxNLsc03Cf.6BBBhx9wDRdBCQVtyesWSQ'
}

 
class Card_Creater:
    
    
    def __init__(self) -> None:
        self.dic_type_path={"Creature":"card_info/creature.txt","Land":"card_info/land.txt","Sorcery":"card_info/sorcery.txt","Instant":"card_info/Instant.txt"}
        self.dic_cards_path={"Creature":"cards/creature","Land":"cards/land","Sorcery":"cards/sorcery","Instant":"cards/Instant"}
        
        self.client = OpenAI(api_key="sk-BXIUJfFqAg1XqqTW7o5tQK9YyhyPQbwdNt9sMm4RIZuiStaW",base_url="https://api.chatanywhere.tech")
        

        self.COOKIE='eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..O-uXyBV7S6PvSfZe.yYNfq1q8qfDMHzkSwaL0tmhkdmG3qJkxoatWKgg8_moTKP0AhisFWCyPOxqPRkwL73_gPbm-hFat4zZKLLxK8CiGHJ15NCAJQuODiuLo28G18iThI5-jKLPgmZREGeIYOl1SsDCRKpDMBf_nbqj1RjMcc1aDbrC5mscjjtUiXjsnyhrmKNe4b7Dug7tpe39_ImAxMYcH5Xz8skGE4I7eaqCruW2WxZBHHyfqkQ1B5uF3m01aNs_bQyt--5Ygj4VsiAwDTwLOJe4jt33AnI3cYFs3bPzv09YS68ykVf1dYu1KrHyLHXkERxWjBaxodmqIanKVW980lq7JNLZc4NRccCWIGE3JUj_X1TB-xxJw3uzCjpWFIHOsGFr8E3h4XiQiIoLDDYl5CksM-YJ9Cqv3RSXubJ4048H6NYyTyeKqQVzt3_gOP1cVPUCl584oY6XSy5c284YQZXQPRHMeqJxDGM8QuyM19GNeuldFbpj3rmAooKbDhucoV76aaemS0Dm6I37ByOsXgBs1yqOFy_XwIUeVz53XqSdE5goBLb3LFZj8ARqZCGDfysupeODwpsdw6Z_quCiyumadIxWVaWF6ib2jF_-hMGDokmop7F0byNJ4gGEMg8BdF1GTtcoeJJ06mt_fniBwZcT6a2qGD94TggUg4lCIcYDhOewKNZagJPCIPf2j0mEAyw2f2X4LLCoJ6hlSdXVZWGZ6Gu8YC3GSBeUtEk0HykpGcdFaX6CwsvdLE-HfGTu5daMJVBK52XoacHYqbMxgR4b5VVoo4LEJK7hDQLwZjrKeCHxkt8sV8_NY7rFQZCBQltf8l0K3JBVURvnnv0XsOPISJYbxhg-ERf7GFcTYnDPx_Py84OooHGCdFZz6E9paUjEtKx25p07Z65ZpyOueLHuU-pLuXPNBpDLP2YcmWhNENxjZa1WPgMIBhXKoKfZFPLcgxTX5tRn1e7h4u5mZTuaiDj71x7UlT_k-FB3ZLZlEInDa7E8xptBUA7P0sC1TcMPy891hloLCpZB2gLPCidnGUcHbXfCdFlubuz70Z4ErHFKKEESF53u8O9qC6YNwTVS1GdSsjI6Y5cgypf7a4LVzd-K2Ev2AyAb3LenmIjB2hrinStXaFKqfhhfeSgImMgQZ7caopY5IrClVAgYWX5y5GO5ziQFBXzW06IcHUk--t5KU2Sa4ToI4LKmvyc0Q_QRD9Rz8fTt2OfmyAV69S9yVKUh5Xyl0DI3cxkzXJKIBvml3p7QJE4lTLn4x3jLiFJx9oSJLFRXKtk65nK5AtHRAysOZYOFbPT7UafiqaFivT4JZto517Q1iUeLrPAgXnpZ5SlJsapxhFz7LbCVWdHCf6HHjYaGJK8elfKdokKB7fs1fQM72SjUCdUHQTeol05we0jpYRstggvIEhm9lOKfoL2QLfcoXd6xe1_UgnzJ6Qn9maJg2I0x8I6FSkPNGf1f1TIydQgntriGp40JX2cEvGLaGDcqO5wEuU-99D4zmq9IABYenXWVPCVeCjzNBPAmkL-ydODXda_NKtOU_BYORLyc8zKdTnpngsCfrlD0MCEmQQ36ATXZSTqUkpToiz3R2WY4yDqVx9qftqn9k7_s1GJz5iXt6U2nDU5B6J70bMPTUA4sHijRrFxd-04Ld67y8O6R6pRw4DoqpeLcvai28jEqYIzKXZHW7Iq0L9tdB1wRpXoOgjVdLNpd2jip-XnFVM4f2YHfKEPp1Q0G8ysvBoTw_ohD9thbNdYRcK9n2k5whP7Dr4cRudRNiNwyvUDjrJM0w0PEYrcUp-KSpZojJUQbZ021nc3ylvpaj3qykOnhy0HDrfd6deY5zZ2yHNaAL7iF1ZtHPn5HIq4j-GeAXBKrz4I_KMyrzw5z_D3eKfYhscjVn9RYwTlpO2gqxz1vPxonoPoEWg7zrPGuFpLKM263MUbf0lZCLQiykgJmgj66H2VNKEfCukg2Ka200DuAtkXa5crciFmqBohkgIZJfC5oBcqdA3Cc-07byosdGnARevevcamCV9Qrzjnyjs18BkTnPYaxT1Je7Qu4HDBHF3cQEIq7E9U1s8V6yCrNq8MaMohL1sUJ774qMcxawUTtm6OQyFOFnarCPv8rA2rHAMhxHFSufhvBUkkQpq0sxKKpt0URq8UjiFMC2Y7mgPgfld9rPL-vHCaYtl1m7X0m_ovDL5FQB7OfLqj2oMRvAdMIuELY4tIpK7uTMWKBtul5_V8RRFGePYuTh3GY0STNl7-dL_unzQtUkhP2VnvnAwAz76olE4Rmh-p3LGbnE5TfZsnCcRBFGjV1odHU6pW80f3Zrt4L-XVdsZ3rN3M-UkD-0eo0mBmMyCHzD_VCn3TDJsAPyYqR8cGUbHp6As5kKnT2lIEAwxSEgzz3qq8bXul-Ca20a5C90ncxuEMa5QoKtYpieki5YLo706JBTnRUF75qB7-NzqSK2pCJ0XKOcQ5wHN1Njz_Pj2XS-pYgZODI-JjWCNNXrh3vn_5sFE2_9ZJropBudlMBZCurdYVe5j5P7QxQ85Y3ohYIB37gIsEYnrdYyR3MvLwuOlOtgV6yoFZfozrUjojrT-VKgIgUAAFiGq70mF1hRn8otJWK8j4fqONRY2r_IPppdgHyrqo173Lca-wnF8tEPX_9nkr8FtAjliOVn940Ua9PQfgyu3_qoydKJiabZMCf6WNhp8VKj_qJI9beOzGHkJ-gmCsCemJ-rZsKjFz19V-fxBuZQhSA1Hi2DITIsUA-Kc4IdykPf96nAsS1Ugdp1H9TalWjolGMRXYfSR3PzZa3nek-mTlce8WZfIYIM0K5Fpulhy20bmTgd8AUcH0al7Lr7XOf_rg-O35Il0WFKgEJKQSdXT-9qoMjQ_5kE_MLiYhqwddpa11IMiymeh8NTFUrjXBIPkHNK45qPdG7itZvqf64IkoXB6Uw-QeEJUG9SG0KaEjojgDAjv97lC-fsh4PClq5dJmAPUsY_h8sQbAuqD1eqBOcs0xicOWYfjGqMesz3cRe0Nc4egJZRsEHRuI-UN5wsEr8HKlzwvGaKdXvJ6pPw6H0EhHJQYD-ZF-cG0ZC2uw9Nq6QUlKBnVgTCAj4hVNXG3sU2b9sN6sU6cchezIjVwMKLd5Bi0Ylbt7N-DdsLfkf66KhWUw0cDwKLVD_NAKoEGC5QtwyZ9QKjfxDvzVzy4Drx8JL9ISVaegtZapXB_pLjMvnBgtgBvbBPrC6lRIwYRdvA3MHyGCycInbSoaFnL3zwRDkoCr6-SFiMVMdk-eQVXGNlDNG13LOnNeRk8q44Ceyvn3L9eV8UJj0Hh10tBV1d5Qdt9TBNAS7Q-IWHtlJJ_ZYnylBxT4bNd1MizyHLYrYxNLsc03Cf.6BBBhx9wDRdBCQVtyesWSQ'
        self.llm = GPT4OpenAI(token=self.COOKIE, headless=False,
                        model='gpt-4' # DALL-E 3 only works with gpt-4
                        )

    
    def generate_prompt(self,params):
        print(params)
        if params["power"]!=0 or params["toughness"]!=0:
            power,toughness=params["power"],params["toughness"]
            power_toughness=f"攻击力{power}，生命值{toughness}"
        else:
            power_toughness=""
        resource_cost=params["mana_cost"].split(" ")
        resource_cost_str="此对象需要的资源是："
        for i,type_rec in zip(range(len(resource_cost)),["人口","追随者","信众","矿石","马"]):
            
            resource_cost_str+=f"{resource_cost[i]}个{type_rec} "
        color_scheme=["水","金","火","木","土"]

        name,type,description,color_scheme=params["name"],params["type"],params["description"],color_scheme[params["color_scheme"]]
        result = f"""
帮我写一下图片的样貌
对象是{name}
对象定位是{type}

然后根据以下描述，觉得这个对象是否强或者弱，创建的图片会根据这个角色是否强或者弱，来决定图片的风格
对象描述是{description}
{power_toughness}
{resource_cost_str}
在五行中，属于{color_scheme}

图片里不可以包含字
请帮我描述一下这个对象的样子，只需描述即可，不用说别的
        """
        return result


    #
    def create_image_prompt(self,prompt):
        #print(self.messages_Creature)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a creative assistant specialized in generating images with an ancient Chinese theme. You will create images based on the attributes and strengths provided, ensuring they reflect the traditional Chinese aesthetic and cultural elements."
            },{
                "role": "user",
                "content": prompt,
            }]

        )

        print(response.choices[0].message.content)
        return response.choices[0].message.content
        
            
        

    

    def create_image_case2(self,prompt):
        
        img_bytes = self.llm.generate_image(f"帮我画一张图，{prompt}，风格：中国古代")
        
        return img_bytes
    
def read_json(path):
    with open(path, "r") as f:
        card_data = json.load(f)
    return card_data
def main():
    card_Creater = Card_Creater()
    card_data = read_json(path="test_example.json")
    for para in card_data:
        prompt1=card_Creater.generate_prompt(para)
        print(prompt1)
        prompt2=card_Creater.create_image_prompt(prompt1)
        bytes=card_Creater.create_image_case2(prompt2)
        with open(para["image_path"],"wb") as f:
            f.write(bytes)

if __name__=="__main__":
    main()
