from PIL import Image


class ImageBuilder:

    def build(self, image_paths, output_path):

        base = None

        for path in image_paths:

            layer = Image.open(path).convert("RGBA")

            if base is None:
                base = layer
            else:
                base = Image.alpha_composite(base, layer)

        base.save(output_path)