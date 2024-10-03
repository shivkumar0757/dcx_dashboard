class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def dfs(node, K):
    if not node:
        return []
    if not node.left and not node.right:
        return [1]
    left_distances = dfs(node.left, K)
    right_distances = dfs(node.right, K)
    for ld in left_distances:
        for rd in right_distances:
            if ld + rd <= K:
                result[0] += 1
    distances = [d + 1 for d in left_distances + right_distances if d + 1 <= K]
    return distances

# Build tree from level order input
def build_tree(levels):
    if not levels or levels[0][0] == -1:
        return None

    # Initialize the root node
    root = TreeNode(levels[0][0])
    queue = [root]  # Queue to keep track of nodes at the current level

    # Start building the tree level by level
    current_index = 0  # Index to keep track of the current parent node in the queue

    for i in range(1, len(levels)):
        current_level = levels[i]
        for j in range(len(current_level)):
            if current_level[j] == -1:
                continue  # Skip if the node is empty (-1)

            # Create the new node
            node = TreeNode(current_level[j])

            # Assign the new node to its correct parent
            parent = queue[current_index]
            if not parent.left:
                parent.left = node
            else:
                parent.right = node
                # Move to the next parent in the queue
                current_index += 1

            # Add the new node to the queue
            queue.append(node)

    return root

# Input and Test
if __name__ == '__main__':
    # Use sys.stdin.read() to read all input at once
    import sys
    data = sys.stdin.read().splitlines()

    if len(data) < 2:
        print("Invalid input")
        sys.exit(1)

    K = int(data[0].strip())
    n = int(data[1].strip())
    levels = [list(map(int, line.strip().split())) for line in data[2:] if line.strip()]

    result = [0]
    root = build_tree(levels)
    dfs(root, K)
    print(result[0])


