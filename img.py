from PIL import Image
import os
import sys

# Attempt to register HEIF opener to support .heic / .heif files
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print("Warning: pillow_heif not installed. .heic format won't be supported.")
    print("Run: pip install pillow-heif")


def convert_to_jpg(input_path, output_path=None):
    """
    Converts an image of any format to JPG.
    """
    try:
        # Open the image file
        img = Image.open(input_path)
        
        # If output_path is not provided, create one by changing the extension
        if not output_path:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}.jpg"
            
        # JPEG doesn't support transparency, so we must convert images that have 
        # an alpha channel (like PNG or WebP) to standard RGB first.
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        # Save it as JPG
        img.save(output_path, "JPEG")
        print(f"✅ Successfully converted '{input_path}' to '{output_path}'")
        
    except Exception as e:
        print(f"❌ Error converting image: {e}")

def compress_to_kb(input_path, target_kb, output_path=None):
    """
    Compresses an image to be under the specified target size (in KB).
    It adjusts the JPEG quality and reduces resolution if necessary.
    """
    try:
        img = Image.open(input_path)
        
        if not output_path:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_{target_kb}kb.jpg"
            
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
            
        target_bytes = target_kb * 1024
        
        # Check if the highest quality is already small enough
        img.save(output_path, "JPEG", quality=95)
        if os.path.getsize(output_path) <= target_bytes:
            print(f"✅ Successfully created '{output_path}'. Size: {os.path.getsize(output_path)/1024:.2f} KB")
            return

        # Binary search for the best quality between 5 and 95
        low = 5
        high = 95
        best_quality = 5
        
        while low <= high:
            mid = (low + high) // 2
            img.save(output_path, "JPEG", quality=mid)
            if os.path.getsize(output_path) <= target_bytes:
                best_quality = mid
                low = mid + 1  # Try to increase quality
            else:
                high = mid - 1 # Need more compression
                
        # Save with the best found quality
        img.save(output_path, "JPEG", quality=best_quality)
        
        # If it's still too large (even at lowest quality), resize the image dimensions
        size = os.path.getsize(output_path)
        if size > target_bytes:
            print(f"Image too large. Shrinking resolution to meet {target_kb} KB target...")
            scale = 0.9
            while size > target_bytes and scale > 0.1:
                new_size = (int(img.width * scale), int(img.height * scale))
                resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
                resized_img = img.resize(new_size, resample_filter)
                resized_img.save(output_path, "JPEG", quality=best_quality)
                size = os.path.getsize(output_path)
                scale -= 0.1
                
        final_kb = os.path.getsize(output_path) / 1024
        print(f"✅ Successfully created '{output_path}'. Final size: {final_kb:.2f} KB (Target: < {target_kb} KB)")

    except Exception as e:
        print(f"❌ Error compressing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # The user passed the path via terminal argument (or dragged & dropped)
        path = sys.argv[1]
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            compress_to_kb(path, int(sys.argv[2]))
        else:
            convert_to_jpg(path)
    else:
        # The user ran the script normally, prompt them for the path!
        print("--- Image Converter & Compressor ---")
        user_path = input("Enter or drag-and-drop the image path here: ").strip()
        
        # Remove surrounding quotes which Windows terminal sometimes adds
        if user_path.startswith('"') and user_path.endswith('"'):
            user_path = user_path[1:-1].strip()
        elif user_path.startswith("'") and user_path.endswith("'"):
            user_path = user_path[1:-1].strip()
            
        if os.path.exists(user_path):
            action = input("Type '1' to convert to JPG, or '2' to compress to a target KB limit: ").strip()
            if action == '2':
                kb_limit = input("Enter the maximum allowed size in KB (e.g., 500): ")
                if kb_limit.isdigit():
                    compress_to_kb(user_path, int(kb_limit))
                else:
                    print("❌ Invalid KB amount entered.")
            else:
                convert_to_jpg(user_path)
        else:
            print(f"❌ Error: Could not find any file at '{user_path}'. Please check the path and try again.")
