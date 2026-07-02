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