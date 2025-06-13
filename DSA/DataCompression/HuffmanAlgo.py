import heapq
from collections import defaultdict
import sys
import os

# Node class for Huffman Tree
class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    # For priority queue comparison (min-heap)
    def __lt__(self, other):
        # Primary comparison by frequency
        if self.freq != other.freq:
            return self.freq < other.freq
        
        # Secondary comparison for consistency when frequencies are equal
        # Use id() for unique comparison to avoid infinite recursion
        return id(self) < id(other)
    
    # We always combine the two smallest-frequency nodes first, so if two nodes have same frequency, it doesn't matter which go first -> for which we use unrelated parameter id()
    # id() is a built-in function, which returns identity of an object (int) [memory address where the object is stored]
    # when we compare nodes: nodeA > nodeB {Python translates it to nodeA.__lt__(nodeB)}
    
    def __eq__(self, other):
        return self.freq == other.freq and id(self) == id(other)
    
    # True → same object
    # False → different objects, even if same content
    # Helps avoid ambiguity in heapq when comparing nodes in the edge cases

# Function to create a new node
def create_node(char, freq, left=None, right=None):
    return Node(char, freq, left, right)

# Function to encode characters and generate Huffman codes
def encode(root, code, huffman_codes):
    if root is None:
        return
    
    # If it's a leaf node, assign the code
    if root.left is None and root.right is None:
        # Handle single character case - assign "0" if no code exists
        huffman_codes[root.char] = code if code else "0"
        return
    
    # Traverse left with '0' and right with '1'
    if root.left:
        encode(root.left, code + "0", huffman_codes)
    if root.right:
        encode(root.right, code + "1", huffman_codes)

# Function to decode Huffman-encoded string
def decode_string(root, encoded_string):
    if not encoded_string or root is None:
        return ""
    
    # Handle single character case
    if root.left is None and root.right is None:
        # For single character, return the character repeated for each bit
        return root.char * len(encoded_string)
    
    decoded_chars = []
    current_node = root
    
    for bit in encoded_string:
        # Navigate the tree based on the bit
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right
        else:
            # Skip invalid characters
            continue
        
        # Check if current_node is None (shouldn't happen with valid encoding)
        if current_node is None:
            print("Warning: Invalid bit sequence encountered during decoding")
            break
        
        # If we reach a leaf node, add the character and reset to root
        if current_node.left is None and current_node.right is None:
            decoded_chars.append(current_node.char)
            current_node = root
    
    # Check if we ended in the middle of a code (incomplete sequence)
    if current_node != root:
        print("Warning: Incomplete bit sequence at end of encoded string")
    
    return ''.join(decoded_chars)

# Main Huffman function
def huffman(input_text):
    if not input_text:
        print("Error: Input text is empty")
        return False
    
    print(f"Processing text of length: {len(input_text)}")
    
    # Calculate frequency of each character
    frequency_map = defaultdict(int)
    for char in input_text:
        frequency_map[char] += 1
    
    print(f"Character frequencies: {dict(frequency_map)}")
    
    # Priority queue to store nodes of Huffman Tree
    priority_queue = []
    
    # Create leaf nodes and add them to priority queue
    for char, freq in frequency_map.items():
        node = create_node(char, freq)
        heapq.heappush(priority_queue, node)
    
    # Handle single character case
    if len(priority_queue) == 1:
        root = priority_queue[0]
        print("Single character detected - using special handling")
    else:
        # Build Huffman Tree by combining nodes
        while len(priority_queue) > 1:
            # Pop two nodes with minimum frequency
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            
            # Create new internal node with combined frequency
            combined_freq = left.freq + right.freq
            merged_node = create_node(None, combined_freq, left, right)
            
            # Push back to priority queue
            heapq.heappush(priority_queue, merged_node)
        
        # Root of the Huffman tree
        root = priority_queue[0]
    
    # Generate Huffman codes
    huffman_codes = {}
    encode(root, "", huffman_codes)
    
    print(f"Generated codes: {huffman_codes}")
    
    # Write Huffman codes to file
    try:
        with open("HuffmanCodes.txt", "w", encoding='utf-8') as huffman_codes_file:
            huffman_codes_file.write("Huffman Codes:\n")
            for char, code in sorted(huffman_codes.items()):
                # Handle special characters for better display
                if char == '\n':
                    display_char = "'\\n'"
                elif char == '\t':
                    display_char = "'\\t'"
                elif char == '\r':
                    display_char = "'\\r'"
                elif char == ' ':
                    display_char = "' '"
                elif ord(char) < 32 or ord(char) > 126:  # Non-printable characters
                    display_char = f"'\\x{ord(char):02x}'"
                else:
                    display_char = f"'{char}'"
                huffman_codes_file.write(f"{display_char} -> {code}\n")
        print("✓ Huffman codes written to HuffmanCodes.txt")
    except IOError as e:
        print(f"Error writing Huffman codes: {e}")
        return False
    
    # Encode the original text
    encoded_string = ''.join(huffman_codes[char] for char in input_text)
    
    # Write compressed string to file
    try:
        with open("CompressedString.txt", "w", encoding='utf-8') as compressed_file:
            compressed_file.write("Compressed String:\n")
            compressed_file.write(encoded_string + "\n")
        print("✓ Compressed string written to CompressedString.txt")
    except IOError as e:
        print(f"Error writing compressed string: {e}")
        return False
    
    # Decode the compressed string
    decoded_text = decode_string(root, encoded_string)
    
    # Write decoded text to file
    try:
        with open("DecodedText.txt", "w", encoding='utf-8') as decoded_file:
            decoded_file.write("Decoded Text:\n")
            decoded_file.write(decoded_text)
        print("✓ Decoded text written to DecodedText.txt")
    except IOError as e:
        print(f"Error writing decoded text: {e}")
        return False
    
    # Verification
    if decoded_text == input_text:
        print("✓ SUCCESS: Decoded text matches original!")
    else:
        print("✗ ERROR: Decoded text does not match original!")
        print(f"Original length: {len(input_text)}")
        print(f"Decoded length: {len(decoded_text)}")
        
        # Debug information
        print("\nFirst 100 characters comparison:")
        print(f"Original: {repr(input_text[:100])}")
        print(f"Decoded:  {repr(decoded_text[:100])}")
        
        # Find first difference
        min_len = min(len(input_text), len(decoded_text))
        for i in range(min_len):
            if input_text[i] != decoded_text[i]:
                print(f"First difference at position {i}: '{input_text[i]}' vs '{decoded_text[i]}'")
                break
        
        return False
    
    # Display compression statistics
    original_bits = len(input_text) * 8  # 8 bits per ASCII character
    compressed_bits = len(encoded_string)
    
    if original_bits > 0:
        compression_ratio = (1 - compressed_bits / original_bits) * 100
        space_saved = original_bits - compressed_bits
        
        print(f"\n📊 Compression Statistics:")
        print(f"   Original size: {len(input_text)} characters ({original_bits} bits)")
        print(f"   Compressed size: {compressed_bits} bits")
        print(f"   Space saved: {space_saved} bits")
        print(f"   Compression ratio: {compression_ratio:.2f}%")
    
    return True

# Main function
def main():
    print("="*50)
    print("\t\tWELCOME TO HUFFMAN ALGORITHM")
    print("="*50)
    
    # Define input file path (modify as needed)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, "new_text.txt")
    
    # Try to read from file first
    input_text = None
    if os.path.exists(input_file_path):
        try:
            with open(input_file_path, "r", encoding='utf-8') as input_file:
                input_text = input_file.read()
            print(f"✓ Successfully read from '{input_file_path}'")
        except IOError as e:
            print(f"✗ Error reading file '{input_file_path}': {e}")
    else:
        print(f"File '{input_file_path}' not found.")
    
    # Use sample text if file reading failed
    if not input_text or not input_text.strip():
        print("Using sample text for demonstration...")
        input_text = "This is a sample text for Huffman encoding demonstration! It contains repeated characters."
        print(f"Sample text: {input_text}")
    
    # Process the text
    success = huffman(input_text)
    
    if success:
        print("\n🎉 Huffman encoding/decoding completed successfully!")
        print("Check the generated files:")
        print("  - HuffmanCodes.txt (character codes)")
        print("  - CompressedString.txt (encoded binary string)")
        print("  - DecodedText.txt (decoded original text)")
    else:
        print("\n Huffman encoding/decoding failed!")
        return 1
    
    return 0

# Entry point
if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)