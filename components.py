"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import logging
import streamlit as st
import constants as ct


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")


def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
        st.markdown("こちらは対話型の商品レコメンド生成AIアプリです。「こんな商品が欲しい」という情報・要望を画面下部のチャット欄から送信いただければ、おすすめの商品をレコメンドいたします。")
        st.markdown("**入力例**")
        st.info("""
        - 「長時間使える、高音質なワイヤレスイヤホン」
        - 「机のライト」
        - 「USBで充電できる加湿器」
        """)


def display_conversation_log():
    """
    会話ログの一覧表示
    """
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=ct.USER_ICON_FILE_PATH):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
                display_product(message["content"])




def display_product(result):
    """
    商品情報の表示
    """
    logger = logging.getLogger(ct.LOGGER_NAME)
    # --- 修正ポイント1: 安全な辞書変換 ---
    product = {}
    try:
        product_lines = result[0].page_content.strip().split("\n")
        for line in product_lines:
            if ": " in line:
                parts = line.split(": ", 1) # 最初の": "だけで分割
                product[parts[0].strip()] = parts[1].strip()
    except Exception as e:
        logger.error(f"パースエラー: {e}")
        st.error("商品データの解析に失敗しました。")
        return
    st.markdown("以下の商品をご提案いたします。")
    # --- 修正ポイント2: .get() を使ってエラーを回避 ---
    # product['id'] ではなく product.get('id', '不明') と書くことで、
    # キーがなくてもエラーにならずに処理を続行できます。
# --- 在庫状況の判定（定数を使用） ---
    stock = product.get('stock_status', ct.STOCK_NONE)
    
    if stock == ct.STOCK_FEW:
        # 「残りわずか」：黄色背景 + ⚠️
        # st.warning(icon=ct.ICON_WARNING, message=ct.STOCK_FEW_MESSAGE)
        st.warning(f"{ct.ICON_WARNING} {ct.STOCK_FEW_MESSAGE}")
    elif stock == ct.STOCK_NONE:
        # 「なし」：赤色背景 + ❗
        # st.error(icon=ct.ICON_ERROR, message=ct.STOCK_NONE_MESSAGE)
        st.error(f"{ct.ICON_ERROR} {ct.STOCK_NONE_MESSAGE}")

        # Adding missing indented block for st.success
        st.success(f"""
            商品名：{product.get('name', '名称未設定')}（商品ID: {product.get('id', 'N/A')}）\n
            価格：{product.get('price', '価格情報なし')}
        """)
    else:

        

        st.code(f"""
            商品カテゴリ：{product.get('category', 'その他')}\n
            メーカー：{product.get('maker', '不明')}\n
            評価：{product.get('score', '-')}({product.get('review_number', '0')}件)
        """, language=None, wrap_lines=True)
    # 画像パスのチェック
    file_name = product.get('file_name')
    if file_name:
        st.image(f"images/products/{file_name}", width=400)
    st.code(product.get('description', '説明はありません。'), language=None, wrap_lines=True)
    st.markdown("**こんな方におすすめ！**")
    st.info(product.get("recommended_people", "すべての方におすすめです。"))
    st.link_button("商品ページを開く", type="primary", use_container_width=True, url="https://google.com")