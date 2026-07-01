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