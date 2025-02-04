import re
import requests
import time

def single_regex(pattern, target_string):
    data = re.findall(pattern, target_string)
    return data[0] if data else ''

output_data = "Instrument No\tDoc ID\tParty Code\tParty Name\tCross Party Name\tRec Date\tDoc Type\tTown\tBook\tPage\tPDF File Name\n"
with open ("Output.txt",'w') as OP:
    OP.write(output_data)
    
with open("input_instrument_no.txt", "r") as file:
    data_list = [line.strip() for line in file]   

for instrument_no in data_list:
    main_url = "http://camden.newvisionsystems.com/SearchAnywhere/api/search"

    headers = {"accept":"application/json, text/plain, */*",
        "accept-encoding":"gzip, deflate",
        "accept-language":"en-GB,en;q=0.9",
        "connection":"keep-alive",
        "content-length":"68",
        "content-type":"application/json;charset=UTF-8",
        "host":"camden.newvisionsystems.com",
        "origin":"http://camden.newvisionsystems.com",
        "referer":"http://camden.newvisionsystems.com/SearchAnywhere/",
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}
        
    payload = '{"FileNumber":'+str(instrument_no)+',"MaxRows":0,"RowsPerPage":0,"StartRow":0}'

    content_response = requests.post(main_url, headers = headers, data = payload)
    response_code = content_response.status_code
    print(response_code)
    content = content_response.text
    time.sleep(5)

    with open('Search_Page.html', 'w', encoding='utf-8') as SP:
        SP.write(content)
        
    blocks = re.findall(r'(doc\_id\"\:[\w\W]*?partyR\_label)',str(content))
    # block = blocks[0]
    cn = 1
    for block in blocks:
       
        doc_id = single_regex(r'doc\_id\"\:([^>]*?)\,',str(block))
        party_code = single_regex(r'party_code\"\:([^>]*?)\,',str(block))
        party_name = single_regex(r'\"party_name\"\:([^>]*?)\,',str(block))
        cross_party_name = single_regex(r'cross_party_name\"\:([^>]*?)\,',str(block))
        rec_date = single_regex(r'rec_date\"\:\"(\d{4}\-\d{2}-\d{2})',str(block))
        doc_type = single_regex(r'doc_type\"\:([^>]*?)\,',str(block))
        town = single_regex(r'town\"\:([^>]*?)\,',str(block))
        book = single_regex(r'book\"\:([^>]*?)\,',str(block))
        page = single_regex(r'page\"\:([^>]*?)\,',str(block))
        

        pdf_url = "http://camden.newvisionsystems.com/SearchAnywhere/api/pdf"

        pdf_headers = {"accept":"application/json, text/plain, */*",
            "accept-encoding":"gzip, deflate",
            "accept-language":"en-GB,en;q=0.9",
            "connection":"keep-alive",
            "content-length":"82",
            "content-type":"application/json;charset=UTF-8",
            "host":"camden.newvisionsystems.com",
            "origin":"http://camden.newvisionsystems.com",
            "referer":"http://camden.newvisionsystems.com/SearchAnywhere/",
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"}

        pdf_payload = '{Token: null, RecaptchaResponseV3: "", ID:'+str(doc_id)+', StartPage: " 1", Pages: ""}'

        pdf_content = requests.post(pdf_url, headers = pdf_headers, data = pdf_payload)
        pdf_response = pdf_content.status_code
        print(pdf_response)

        if pdf_response == 200:
            pdf_file_name = f'{cn}_{doc_id}.pdf'
            if 'application/pdf' in pdf_content.headers.get('Content-Type', ''):
                # Save the PDF file
                with open(pdf_file_name, 'wb') as pdf_file:
                    pdf_file.write(pdf_content.content)
                print(f"PDF file saved as {pdf_file_name}")
                cn += 1
            else:
                pdf_file_name = "Error"
                print("The response content is not a PDF.")
            
            output_data = f"{instrument_no}\t{doc_id}\t{party_code}\t{party_name}\t{cross_party_name}\t{rec_date}\t{doc_type}\t{town}\t{book}\t{page}\t{pdf_file_name}\n"
            with open ("Output.txt",'a') as OP:
                OP.write(output_data)
                    
        else:
            print("Failed to download PDF. Check the doc_id and payload.")
            pdf_file_name = "Error"
            
            output_data = f"{instrument_no}\t{doc_id}\t{party_code}\t{party_name}\t{cross_party_name}\t{rec_date}\t{doc_type}\t{town}\t{book}\t{page}\t{pdf_file_name}\n"
            with open ("Output.txt",'a') as OP:
                OP.write(output_data)
        
    print("ID Completed: ", instrument_no)
    
print("Completed")