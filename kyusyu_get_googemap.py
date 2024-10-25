import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

# Google Mapsの検索URLから共有リンクを取得する関数
def get_share_url(search_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    try:
        # Google Mapsのページにアクセス
        driver.get(search_url)
        time.sleep(40)  # ページが完全に読み込まれるまで待機
        
        # 共有ボタンをクリック
        try:
            share_button = driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[5]/button/span')
            driver.execute_script("arguments[0].click();", share_button)
            # print(share_button)
            # share_button.click()
        except Exception as e:
            print(f"Error finding share button: {e}")
            return None
        
        time.sleep(30)  # 共有ウィンドウが開くまで待機
        
        # 共有リンクを取得
        try:
            share_url_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="modal-dialog"]/div/div[2]/div/div[2]/div/div/div/div[3]/div[2]/div[2]/input'))
            )
            share_url = share_url_element.get_attribute('value')
            return share_url
        except Exception as e:
            print(f"Error finding share URL: {e}")
            return None

    except Exception as e:
        print(f"Error getting share URL for {search_url}: {e}")
        return None
    finally:
        driver.quit()

# CSVファイルを読み込む
input_file = '九州温泉道2.csv'
output_file = '九州温泉道_with_share_urls.csv'

df = pd.read_csv(input_file)

# 共有URLを保存するための新しい列を追加
df['Share URL'] = None

# tqdmを使って進捗バーを表示
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    search_url = row['Google map']
    if pd.notna(search_url):  # URLがNaNでない場合
        share_url = get_share_url(search_url)
        print(share_url)
        if share_url:
            df.at[index, 'Share URL'] = share_url
        else:
            print(f"Failed to get shared URL for {search_url}")

# 結果を新しいCSVファイルに保存
df.to_csv(output_file, index=False, encoding='utf-8')

print(f"共有URLを取得し、{output_file} に保存しました。")
exit()

"""
csvの文字化け解消
"""
import pandas as pd

# 文字化けしていたCSVファイルをutf-8で読み取り済み
file_path = '九州温泉道_with_share_urls.csv'

# 読み取ったデータフレームをutf-8で再保存する
output_file_path = '九州温泉道_corrected.csv'

# utf-8で保存し直す
df = pd.read_csv(file_path, encoding='utf-8')
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print(f"データを {output_file_path} に utf-8-sig で保存しました。")
