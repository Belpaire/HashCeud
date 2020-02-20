from Image import Image

#Input reader whaddafak
def read_in_file(file_name):
    imgs = []
    with open(file_name, "r") as input_file:

        # read in header
        header = input_file.readline()
        header = header.replace("\n", "")
        N = int(header)
        tags=set()
        freq=dict()
        id=0
        for line in input_file:
            line = line.replace("\n", "")
            img_data = line.split(' ')
            imgs.append(Image(id,img_data[0],img_data[2:]))
            for tag in img_data[2:]:
                tags.add(tag)
                if freq.get(tag) == None:
                    freq[tag] = 1
                else:
                    freq[tag] = freq[tag]+1
            id += 1

    return [imgs,tags,freq]


def write_output_file(solution_file_name, slides_list=None):
    with open(solution_file_name, "w") as f:

        if slides_list is None:
            slides_list = []

        f.write("{}\n".format(len(slides_list)))

        for slide in slides_list:
            img_ids = [img.id for img in slide.images]
            f.write(' '.join(map(str,img_ids)) + "\n")
