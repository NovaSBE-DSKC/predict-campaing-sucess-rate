def get_display_text(text):
  return text.replace("_", " ") \
    .strip() \
    .lstrip() \
    .lower() \
    .title()
