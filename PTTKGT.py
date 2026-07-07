class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char        # Ký tự được mã hóa (None nếu là nút trong)
        self.freq = freq        # Tần suất xuất hiện
        self.left = None        # Nút con nhánh trái (0)
        self.right = None       # Nút con nhánh phải (1)

    # Nạp chồng toán tử so sánh nhỏ hơn (<)
    # Rất quan trọng để Min Heap biết cách so sánh 2 object Node
    def __lt__(self, other):
        return self.freq < other.freq
class MinHeap:
    def __init__(self):
        self.heap = []

    def get_size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def swap_nodes(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    # Vun đống từ dưới lên (Dùng khi thêm nút mới vào cuối list)
    def heapify_up(self, idx):
        while idx > 0:
            parent_idx = (idx - 1) // 2
            # Nếu nút hiện tại nhỏ hơn nút cha, đổi chỗ đưa nó lên trên
            if self.heap[idx].freq < self.heap[parent_idx].freq:
                self.swap_nodes(idx, parent_idx)
                idx = parent_idx
            else:
                break

    # Vun đống từ trên xuống (Dùng khi lấy nút gốc ra và đưa nút cuối lên thay thế)
    def heapify_down(self, idx):
        smallest = idx
        left_child = 2 * idx + 1
        right_child = 2 * idx + 2
        size = self.get_size()

        # Tìm vị trí của nút có tần suất nhỏ nhất trong 3 nút (cha, con trái, con phải)
        if left_child < size and self.heap[left_child].freq < self.heap[smallest].freq:
            smallest = left_child
            
        if right_child < size and self.heap[right_child].freq < self.heap[smallest].freq:
            smallest = right_child

        # Nếu nút cha không phải là nhỏ nhất, đổi chỗ và đệ quy tiếp tục chìm xuống
        if smallest != idx:
            self.swap_nodes(idx, smallest)
            self.heapify_down(smallest)

    # Thêm một nút mới vào Heap
    def insert(self, node):
        self.heap.append(node)
        self.heapify_up(self.get_size() - 1)

    # Lấy ra và xóa nút có tần suất nhỏ nhất (nút ở gốc)
    def extract_min(self):
        if self.is_empty():
            return None
        
        if self.get_size() == 1:
            return self.heap.pop()

        # Lưu lại nút gốc (nhỏ nhất) để trả về
        min_node = self.heap[0]
        
        # Đưa nút cuối cùng lên làm gốc và xóa phần tử cuối đi
        self.heap[0] = self.heap.pop()
        
        # Tái cấu trúc lại Heap từ đỉnh xuống
        self.heapify_down(0)
        
        return min_node

# ... (Giữ nguyên code class HuffmanNode và MinHeap của bạn ở trên) ...

class HuffmanEncoder:
    def __init__(self):
        self.root = None
        self.codes = {}             # Lưu bảng mã (VD: {'a': '100', 'e': '01'})
        self.reverse_mapping = {}   # Lưu bảng ngược để Phát dùng cho giải mã (VD: {'100': 'a'})

    # 1. Thống kê tần suất xuất hiện của các ký tự trong văn bản
    def make_frequency_dict(self, text):
        freq_dict = {}
        for character in text:
            if character not in freq_dict:
                freq_dict[character] = 0
            freq_dict[character] += 1
        return freq_dict

    # 2. Xây dựng cây Huffman
    def build_tree(self, text):
        freq_dict = self.make_frequency_dict(text)
        min_heap = MinHeap()
        
        # Bước 2.1: Khởi tạo các nút lá và đưa vào Min Heap
        for key, freq in freq_dict.items():
            node = HuffmanNode(key, freq)
            min_heap.insert(node)
            
        # Bước 2.2: Lặp cho đến khi chỉ còn 1 nút duy nhất (Gốc của cây)
        while min_heap.get_size() > 1:
            # Lấy 2 nút có tần suất nhỏ nhất ra khỏi heap
            node1 = min_heap.extract_min()
            node2 = min_heap.extract_min()
            
            # Tạo nút cha với tần suất bằng tổng 2 nút con. 
            # Nút trong (Internal node) không lưu ký tự nên để None.
            merged_freq = node1.freq + node2.freq
            merged_node = HuffmanNode(None, merged_freq)
            merged_node.left = node1
            merged_node.right = node2
            
            # Đưa nút cha ngược lại vào heap
            min_heap.insert(merged_node)
            
        # Nút cuối cùng còn lại chính là gốc của cây
        self.root = min_heap.extract_min()

    # 3. Hàm đệ quy duyệt cây để tạo mã bit (Trái = 0, Phải = 1)
    def make_codes_helper(self, node, current_code):
        if node is None:
            return
        
        # Nếu chạm đến nút lá (có chứa ký tự), lưu mã bit vào từ điển
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_mapping[current_code] = node.char
            return
            
        # Duyệt tiếp xuống nhánh trái (thêm '0') và phải (thêm '1')
        self.make_codes_helper(node.left, current_code + "0")
        self.make_codes_helper(node.right, current_code + "1")

    # Hàm mồi để gọi quá trình đệ quy sinh mã từ Root
    def generate_codes(self):
        current_code = ""
        self.make_codes_helper(self.root, current_code)

    # 4. Mã hóa văn bản gốc thành chuỗi bit nhị phân
    def encode_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text


# ==========================================
# TEST CHẠY THỬ (Dành cho Tâm kiểm tra code)
# ==========================================
if __name__ == "__main__":
    # Đoạn text giả định để test
    text_mau = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    print(f"Văn bản gốc: {text_mau}\n")

    # Khởi tạo bộ mã hóa
    encoder = HuffmanEncoder()
    
    # Thực thi các bước
    encoder.build_tree(text_mau)
    encoder.generate_codes()
    chuoi_da_nen = encoder.encode_text(text_mau)
    
    # In kết quả
    print("1. Bảng mã Huffman được sinh ra:")
    for char, code in encoder.codes.items():
        print(f"   '{char}': {code}")
        
    print(f"\n2. Chuỗi bit sau khi nén:\n{chuoi_da_nen}")
    
    # So sánh độ dài
    so_bit_goc = len(text_mau) * 8 # Giả sử dùng ASCII 8-bit
    so_bit_nen = len(chuoi_da_nen)
    print(f"\n3. Dung lượng gốc: {so_bit_goc} bits")
    print(f"   Dung lượng nén: {so_bit_nen} bits")
# ... (Giữ nguyên phần import và code của Tài Anh, Tâm ở trên) ...

class HuffmanDecoder:
    def __init__(self):
        pass

    # 1. Đệm thêm bit (Padding) cho chẵn 8-bit (1 byte)
    def pad_encoded_text(self, encoded_text):
        # Tính số bit còn thiếu để chia hết cho 8
        extra_padding = 8 - len(encoded_text) % 8
        # Thêm các bit '0' vào cuối chuỗi
        encoded_text += "0" * extra_padding
        
        # Chuyển con số extra_padding thành chuỗi nhị phân dài 8 bit
        # Để kẹp vào phần ĐẦU của chuỗi bit, làm manh mối cho lúc giải mã
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # 2. Chuyển chuỗi bit thành mảng các Byte để lưu xuống file .bin
    def get_byte_array(self, padded_encoded_text):
        b = bytearray()
        # Cắt từng khúc 8 bit một và ép kiểu sang số nguyên (byte)
        for i in range(0, len(padded_encoded_text), 8):
            byte_str = padded_encoded_text[i:i+8]
            b.append(int(byte_str, 2))
        return b

    # 3. Đọc mảng byte từ file, gỡ bỏ phần đệm để lấy lại chuỗi bit gốc
    def remove_padding(self, padded_encoded_text):
        # Lấy 8 bit đầu tiên để biết hồi trước đã đệm thêm bao nhiêu bit
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        
        # Cắt bỏ 8 bit thông tin ở đầu
        padded_encoded_text = padded_encoded_text[8:]
        # Cắt bỏ phần bit đệm ở đuôi
        encoded_text = padded_encoded_text[:-extra_padding]
        
        return encoded_text

    # 4. Thuật toán giải mã: Từ chuỗi bit nén -> Văn bản gốc
    def decode_text(self, encoded_text, root):
        decoded_text = ""
        current_node = root
        
        # Duyệt từng bit 0 và 1
        for bit in encoded_text:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
                
            # Nếu chạm đến nút lá (nút có chứa ký tự)
            if current_node.char is not None:
                decoded_text += current_node.char # Xuất ký tự
                current_node = root               # Quay lại gốc cây để dịch bit tiếp theo
                
        return decoded_text


# ==========================================
# TEST TÍCH HỢP TOÀN HỆ THỐNG (Dành cho Phát kiểm tra)
# ==========================================
if __name__ == "__main__":
    import os

    text_mau = "A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED"
    print(f"--- VĂN BẢN GỐC ---\n{text_mau}\n")

    # --- PHA 1: MÃ HÓA (CỦA TÂM) ---
    encoder = HuffmanEncoder()
    encoder.build_tree(text_mau)
    encoder.generate_codes()
    chuoi_bit_nen = encoder.encode_text(text_mau)
    
    print(f"--- PHA 1: NÉN DỮ LIỆU ---")
    print(f"Chuỗi bit ban đầu ({len(chuoi_bit_nen)} bits): {chuoi_bit_nen}\n")

    # --- PHA 2: LƯU FILE NHỊ PHÂN & GIẢI MÁ (CỦA PHÁT) ---
    decoder = HuffmanDecoder()
    
    # 2.1 Xử lý Padding và lưu file .bin
    chuoi_da_dem = decoder.pad_encoded_text(chuoi_bit_nen)
    mang_byte = decoder.get_byte_array(chuoi_da_dem)
    
    with open("compressed.bin", "wb") as f:
        f.write(bytes(mang_byte))
    print("Đã lưu file nhị phân thành công vào 'compressed.bin'!\n")

    # 2.2 Đọc file .bin và giải mã
    with open("compressed.bin", "rb") as f:
        bit_string = ""
        byte = f.read(1)
        while byte:
            byte_val = ord(byte)
            bits = bin(byte_val)[2:].rjust(8, '0')
            bit_string += bits
            byte = f.read(1)

    chuoi_bit_khoi_phuc = decoder.remove_padding(bit_string)
    
    # Kích hoạt hàm duyệt cây (Dùng cây root do Tâm đã xây dựng)
    van_ban_giai_ma = decoder.decode_text(chuoi_bit_khoi_phuc, encoder.root)

    print(f"--- PHA 2: GIẢI MÁ DỮ LIỆU ---")
    print(f"Khôi phục văn bản: {van_ban_giai_ma}")
    
    if van_ban_giai_ma == text_mau:
        print("\n=> KẾT LUẬN: THÀNH CÔNG! Văn bản giải mã khớp 100% với bản gốc.")
        


