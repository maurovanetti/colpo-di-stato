class Conspirator:

    def __init__(self, name, link_codes_base, link_codes_extra, extra=False):
        self.name = name
        self.links_base = {
            'n': 0,
            'e': 0,
            'w': 0,
            's': 0
        }
        self.links_extra = {
            'n': 0,
            'e': 0,
            'w': 0,
            's': 0
        }
        Conspirator.fill(link_codes_base, self.links_base)
        Conspirator.fill(link_codes_extra, self.links_extra)
        self.extra = extra

    @staticmethod
    def fill(link_codes, links):
        for link_code in link_codes:
            if link_code in 'news':
                links[link_code] = 1
            elif link_code in 'NEWS':
                links[link_code.lower()] = 2

    def links(self):
        if self.extra:
            return self.links_extra
        else:
            return self.links_base

    def can_join(self, direction, other):
        if other is None:
            return False
        link_type = self.links()[direction]
        if link_type is 0:
            return False
        other_direction = 'swen'['news'.index(direction)]
        return link_type == other.links()[other_direction]
