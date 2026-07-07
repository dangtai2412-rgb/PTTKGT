import os
import pickle
import time
from PTTKGT import HuffmanEncoder, HuffmanDecoder

def print_menu():
    print("\n" + "="*45)
    print("  CHƯƠNG TRÌNH NÉN DỮ LIỆU HUFFMAN CODING  ")
    print("="*45)
    print("  1. Nén file (Compress)")
    print("  2. Giải nén file (Decompress)")
    print("  3. Thoát chương trình")
    print("="*45)

def main():
    # Tự động tạo thư mục chứa dữ liệu test nếu chưa có
    os.makedirs("data/input", exist_ok=True)
    os.makedirs("data/output", exist_ok=True)

    encoder = HuffmanEncoder()
    decoder = HuffmanDecoder()

    while True:
        print_menu()
        choice = input("Nhập lựa chọn của bạn (1/2/3): ")

        if choice == '1':
            print("\n--- CHỨC NĂNG NÉN FILE ---")
            input_path = input("Nhập đường dẫn file cần nén (VD: data/input/test.txt): ")
            
            if not os.path.exists(input_path):
                print("[LỖI] Không tìm thấy file! Hãy kiểm tra lại đường dẫn.")
                continue

            # Đọc nội dung file
            with open(input_path, 'r', encoding='utf-8') as file:
                text = file.read()

            if not text:
                print("[LỖI] File rỗng! Thuật toán cần ít nhất 1 ký tự.")
                continue

            print("Đang xử lý nén...")
            start_time = time.time()
            
            # 1. Gọi module của Lộc/Tâm để xây cây và nén
            encoder.build_tree(text)
            encoder.generate_codes()
            encoded_text = encoder.encode_text(text)

            # 2. Gọi module của Phát/Long để đệm bit và chuyển thành byte
            padded_encoded_text = decoder.pad_encoded_text(encoded_text)
            byte_array = decoder.get_byte_array(padded_encoded_text)

            # 3. Lưu file nhị phân
            output_path = input("Nhập đường dẫn lưu file nén (VD: data/output/compressed.bin): ")
            with open(output_path, 'wb') as file:
                file.write(bytes(byte_array))

            # 4. Lưu lại cấu trúc cây Huffman bằng Pickle để sau này phục vụ giải mã
            tree_path = output_path + ".tree"
            with open(tree_path, 'wb') as tree_file:
                pickle.dump(encoder.root, tree_file)
                
            end_time = time.time()
            
            # --- TÍNH TOÁN HIỆU NĂNG (Dành cho Thành viên 5) ---
            kich_thuoc_goc = os.path.getsize(input_path)
            kich_thuoc_nen = os.path.getsize(output_path) + os.path.getsize(tree_path)
            ty_le_nen = (kich_thuoc_nen / kich_thuoc_goc) * 100 if kich_thuoc_goc > 0 else 0

            print(f"\n[THÀNH CÔNG] Đã lưu file nén tại: {output_path}")
            print(f"[THÀNH CÔNG] Đã lưu cấu trúc cây tại: {tree_path}")
            print("\n" + "-"*35)
            print("  BÁO CÁO HIỆU NĂNG NÉN ")
            print("-"*35)
            print(f"Thời gian chạy : {end_time - start_time:.4f} giây")
            print(f"Kích thước gốc : {kich_thuoc_goc} bytes")
            print(f"Kích thước nén : {kich_thuoc_nen} bytes (Bao gồm cây)")
            print(f"Tỷ lệ nén      : {ty_le_nen:.2f}%")
            print(f"Không gian tiết kiệm: {100 - ty_le_nen:.2f}%")
            print("-"*35)

        elif choice == '2':
            print("\n--- CHỨC NĂNG GIẢI NÉN FILE ---")
            input_path = input("Nhập đường dẫn file .bin cần giải nén: ")
            
            if not os.path.exists(input_path):
                print("[LỖI] Không tìm thấy file nén!")
                continue

            tree_path = input_path + ".tree"
            if not os.path.exists(tree_path):
                print(f"[LỖI] Không tìm thấy file cây ({tree_path}). Không thể giải mã!")
                continue

            print("Đang xử lý giải nén...")
            start_time = time.time()
            
            # 1. Phục hồi cấu trúc cây từ file .tree
            with open(tree_path, 'rb') as tree_file:
                root = pickle.load(tree_file)

            # 2. Đọc file nén nhị phân
            with open(input_path, 'rb') as file:
                bit_string = ""
                byte = file.read(1)
                while len(byte) > 0:
                    byte_val = ord(byte)
                    bits = bin(byte_val)[2:].rjust(8, '0')
                    bit_string += bits
                    byte = file.read(1)

            # 3. Gọi module giải mã của Phát/Long
            encoded_text = decoder.remove_padding(bit_string)
            decoded_text = decoder.decode_text(encoded_text, root)

            # 4. Lưu kết quả ra file text
            output_path = input("Nhập đường dẫn lưu file giải nén (VD: data/output/decoded.txt): ")
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(decoded_text)
                
            end_time = time.time()

            print(f"\n[THÀNH CÔNG] Đã khôi phục văn bản gốc và lưu tại: {output_path}")
            print("\n" + "-"*35)
            print("  BÁO CÁO HIỆU NĂNG GIẢI NÉN ")
            print("-"*35)
            print(f"Thời gian chạy: {end_time - start_time:.4f} giây")
            print("-"*35)

        elif choice == '3':
            print("\nCảm ơn bạn đã sử dụng chương trình!")
            break
        else:
            print("\n[LỖI] Lựa chọn không hợp lệ. Vui lòng nhập 1, 2 hoặc 3!")

if __name__ == "__main__":
    main()