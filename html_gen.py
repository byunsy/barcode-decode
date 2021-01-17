"""============================================================================
TITLE: html_gen.py
BY   : Sang Yoon Byun
============================================================================"""
import sys
import numpy as np
import cv2
import decode as dc
import scrape as sc

""" ===========================================================================
                                     MAIN
=========================================================================== """
def main():

    template = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Product Results</title>
        <!-- normalize -->
        <link
        rel="stylesheet"
        href="https://necolas.github.io/normalize.css/8.0.1/normalize.css"
        />
        <!-- font awesome -->
        <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.css"
        integrity="sha256-46qynGAkLSFpVbEBog43gvNhfrOj+BmwXdxFgVK/Kvc="
        crossorigin="anonymous"
        />
        <!-- google fonts api -->
        <link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;900&display=swap"
        />
        <link rel="stylesheet" type="text/css" href="results.css">
    </head>
    <body>
        <!-- Title -->
        <section class="title_section">
            <h1 class="page_title">안녕하세요!</h1>
            <h2>"{product_name}" 에 관한 결과입니다.</h2>
        </section>
        
        <!-- Results -->
        <section class="product_results">
            <h2 class="section_title">COUPANG</h2>

            <div class="results-list">

                <!-- ITEM 1 -->
                <img src="{item1_img}" class="item1" />
                <div class="text1">
                <h3>{item1_name}</h3>
                <ul>
                    <li>{item1_price}원</li>
                    <li>평점: {item1_rating}</li> 
                </ul>
                <a href="{item1_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>
    
                <!-- ITEM 2 -->
                <img src="{item2_img}" class="item2" />
                <div class="text2">
                <h3>{item2_name}</h3>
                <ul>
                    <li>{item2_price}원</li>
                    <li>평점: {item2_rating}</li> 
                </ul>
                <a href="{item2_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 3 -->
                <img src="{item3_img}" class="item3" />
                <div class="text3">
                <h3>{item3_name}</h3>
                <ul>
                    <li>{item3_price}원</li>
                    <li>평점: {item3_rating}</li> 
                </ul>
                <a href="{item3_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 4 -->
                <img src="{item4_img}" class="item4" />
                <div class="text4">
                <h3>{item4_name}</h3>
                <ul>
                    <li>{item4_price}원</li>
                    <li>평점: {item4_rating}</li> 
                </ul>
                <a href="{item4_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 5 -->
                <img src="{item5_img}" class="item5" />
                <div class="text5">
                <h3>{item5_name}</h3>
                <ul>
                    <li>{item5_price}원</li>
                    <li>평점: {item5_rating}</li> 
                </ul>
                <a href="{item5_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 6 -->
                <img src="{item6_img}" class="item6" />
                <div class="text6">
                <h3>{item6_name}</h3>
                <ul>
                    <li>{item6_price}원</li>
                    <li>평점: {item6_rating}</li> 
                </ul>
                <a href="{item6_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 7 -->
                <img src="{item7_img}" class="item7" />
                <div class="text7">
                <h3>{item7_name}</h3>
                <ul>
                    <li>{item7_price}원</li>
                    <li>평점: {item7_rating}</li> 
                </ul>
                <a href="{item7_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 8 -->
                <img src="{item8_img}" class="item8" />
                <div class="text8">
                <h3>{item8_name}</h3>
                <ul>
                    <li>{item8_price}원</li>
                    <li>평점: {item8_rating}</li> 
                </ul>
                <a href="{item8_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 9 -->
                <img src="{item9_img}" class="item9" />
                <div class="text9">
                <h3>{item9_name}</h3>
                <ul>
                    <li>{item9_price}원</li>
                    <li>평점: {item9_rating}</li> 
                </ul>
                <a href="{item9_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>

                <!-- ITEM 10 -->
                <img src="{item10_img}" class="item10" />
                <div class="text10">
                <h3>{item10_name}</h3>
                <ul>
                    <li>{item10_price}원</li>
                    <li>평점: {item10_rating}</li> 
                </ul>
                <a href="{item10_link}" target="_blank"><strong>자세히 보기</strong></a>
                </div>
            </div>
        </section>
    </body>
    </html>
    """

    # Initialize and open default camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Check for any errors opening the camera
    if not cap.isOpened():
        print("Error: Failed to open camera.")
        sys.exit()

    # Keep running until barcode is detected
    while True:

        ret, frame = cap.read()
        if not ret:
            break

        frame = dc.draw_guide(frame)

        # decode barcode if it exists
        barcode_num = dc.decode(frame)

        # if successfully decoded
        if barcode_num:
            print("Detected Barcode:", barcode_num)
            break

        # exit if pressed ESC
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    if barcode_num is None:
        sys.exit()
    
    # use the barcode to identify product
    product = sc.get_product(barcode_num)
    print("Detected Product:", product)

    # refine product name
    refined = sc.refine_keyword(product)
    print("Searching it as :", refined)

    # search Coupang and scrape information
    results = sc.search_coupang(refined)

    # parse the results
    item1, item2, item3, item4, item5, item6, item7, item8, item9, item10 = results

    results_summary = template.format(product_name=refined, 
            item1_img=item1[1], item1_name=item1[0], item1_link=item1[4],
            item1_price=item1[2], item1_rating=item1[3],

            item2_img=item2[1], item2_name=item2[0], item2_link=item2[4],
            item2_price=item2[2], item2_rating=item2[3], 

            item3_img=item3[1], item3_name=item3[0], item3_link=item3[4],
            item3_price=item3[2], item3_rating=item3[3],

            item4_img=item4[1], item4_name=item4[0], item4_link=item4[4],
            item4_price=item4[2], item4_rating=item4[3],

            item5_img=item5[1], item5_name=item5[0], item5_link=item5[4],
            item5_price=item5[2], item5_rating=item5[3],

            item6_img=item6[1], item6_name=item6[0], item6_link=item6[4],
            item6_price=item6[2], item6_rating=item6[3],

            item7_img=item7[1], item7_name=item7[0], item7_link=item7[4],
            item7_price=item7[2], item7_rating=item7[3],

            item8_img=item8[1], item8_name=item8[0], item8_link=item8[4],
            item8_price=item8[2], item8_rating=item8[3],

            item9_img=item9[1], item9_name=item9[0], item9_link=item9[4],
            item9_price=item9[2], item9_rating=item9[3],

            item10_img=item10[1], item10_name=item10[0], item10_link=item10[4],
            item10_price=item10[2], item10_rating=item10[3],
    )

    with open("./results.html", 'w', encoding='utf8') as f:
        f.write(results_summary)
    f.close()

    print()
    print("Job successfully completed.")

if __name__ == '__main__':
    main()