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

class HuffmanEncoder:
    def __init__(self):
        self.root = None
        self.codes = {}       # Bảng mã: ký tự -> chuỗi bit
        self.freq_table = {}  # Bảng tần suất: ký tự -> số lần xuất hiện

    # ----- Đọc file & thống kê tần suất -----
    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def calculate_frequency(self, text):
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        return freq

    # ----- Xây dựng cây Huffman -----
    def build_tree(self, text):
        self.freq_table = self.calculate_frequency(text)

        heap = MinHeap()
        for char, freq in self.freq_table.items():
            heap.insert(HuffmanNode(char, freq))

        # Trường hợp đặc biệt: văn bản chỉ có 1 loại ký tự (VD: "AAAAAA")
        # -> phải tạo thêm 1 nút cha giả để cây có ít nhất 1 cạnh,
        #    nếu không mã sinh ra sẽ rỗng ("").
        if heap.get_size() == 1:
            only_node = heap.extract_min()
            parent = HuffmanNode(None, only_node.freq)
            parent.left = only_node
            self.root = parent
            return self.root

        # Thuật toán tham lam: lặp lại việc lấy 2 node tần suất nhỏ nhất,
        # gộp thành 1 node cha, đưa lại vào heap, cho đến khi chỉ còn gốc.
        while heap.get_size() > 1:
            left = heap.extract_min()
            right = heap.extract_min()
            parent = HuffmanNode(None, left.freq + right.freq)
            parent.left = left
            parent.right = right
            heap.insert(parent)

        self.root = heap.extract_min()
        return self.root

    # ----- Sinh bảng mã bit (duyệt cây, trái = 0, phải = 1) -----
    def generate_codes(self):
        self.codes = {}
        if self.root is None:
            return self.codes
        self._generate_codes_recursive(self.root, "")
        return self.codes

    def _generate_codes_recursive(self, node, current_code):
        if node is None:
            return
        if node.char is not None:  # gặp nút lá -> lưu mã
            # Trường hợp cây chỉ có 1 ký tự, current_code sẽ là "" -> gán "0"
            self.codes[node.char] = current_code if current_code != "" else "0"
            return
        self._generate_codes_recursive(node.left, current_code + "0")
        self._generate_codes_recursive(node.right, current_code + "1")

    # ----- Chuyển văn bản thành chuỗi bit dựa trên bảng mã -----

    def encode_text(self, text):
        if not self.codes:
            self.generate_codes()
        encoded_bits = "".join(self.codes[char] for char in text)
        return encoded_bits

if __name__ == "__main__":
    # Test thử của Tâm
    text_mau = "AABCB"
    encoder = HuffmanEncoder()
    encoder.build_tree(text_mau)
    encoder.generate_codes()

    print("Bảng mã của Lộc sinh ra:", encoder.codes)
    print("Chuỗi nén:", encoder.encode_text(text_mau))
