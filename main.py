from database import Database
from random import randint

class Location:
    def __init__(self, id: int):
        self.database = Database()
        #self.database.show_table()
        self.id, self.location_type, self.location_id = self.database.get_location(id)

    def __str__(self):
        return f"{self.id}\t{self.location_type}\t{self.location_id}"

    def parent_locations(self, location_id=None):
        if location_id is None:
            location_id = self.database.get_location(self.id)[-1]
            parent_locations = [self.id, location_id]
        else:
            location_id = self.database.get_location(location_id)[-1]
            parent_locations = [location_id]

        if location_id == 0 and len(parent_locations) == 2:
            return parent_locations[:1:]
        elif location_id == 0:
            return []
        return parent_locations + self.parent_locations(location_id)

    @staticmethod
    def sort_locations(locations):
        if len(locations) <= 1:
            return locations

        pivot = locations[0]
        children = []
        parents = []
        for location in locations[1::]:
            union = location.parent_locations() + pivot.parent_locations()
            if len(union) == len(set(union)):  # Если общих родителей нет
                if pivot.location_type > location.location_type:
                    parents.append(location)
                elif pivot.location_type < location.location_type:
                    children.append(location)
                else:
                    if len(location.parent_locations()) < len(pivot.parent_locations()):
                        children.append(location)
                    else:
                        parents.append(location)

            elif pivot.id in location.parent_locations():  # Принадлежит ли pivot к детям location
                children.append(location)
            elif location.id in pivot.parent_locations():
                parents.append(location)
            else:
                if pivot.location_type > location.location_type:
                    parents.append(location)
                elif pivot.location_type < location.location_type:
                    children.append(location)
                else:
                    if len(location.parent_locations()) < len(pivot.parent_locations()):
                        children.append(location)
                    else:
                        parents.append(location)
        return Location.sort_locations(parents) + [pivot] + Location.sort_locations(children)


if __name__ == "__main__":
    print(
        Location(randint(1, 16)).parent_locations()
    )

    sort_locations = Location.sort_locations([Location(randint(1, 16)) for i in range(20)])
    for location in sort_locations:
        print(location)
