from dskc.visualization.terminal import markdown_h2


def header(section, sub_section, text, increment_sub_section=True):
    print("\n")
    markdown_h2("{}.{} {}".format(section, sub_section, text))
    print("\n")

    if increment_sub_section:
        sub_section += 1

    return sub_section