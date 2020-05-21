class Parent:

    def inherited_method(self):
        """Duis lacus metus, euismod ut viverra sit amet, pulvinar sed urna."""
        pass

class Example(Parent):
    """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.

    Nam justo sem, malesuada ut ultricies ac, bibendum eu neque. Lorem ipsum 
    dolor sit amet, consectetur adipiscing elit. Aenean at tellus ut velit 
    dignissim tincidunt. Curabitur euismod laoreet orci semper dignissim. 
    Suspendisse potenti. 
    """

    def __init__(self):
        """Vivamus sed enim quis dui pulvinar pharetra."""
        pass

    def documented_method(self):
        """
        Duis condimentum ultricies ipsum, sed ornare leo vestibulum vitae. 

        Sed ut justo massa, varius molestie diam. Sed lacus quam, tempor in 
        dictum sed, posuere et diam. Maecenas tincidunt enim elementum turpis 
        blandit tempus. Nam lectus justo, adipiscing vitae ultricies egestas, 
        porta nec diam. Aenean ac neque tortor. 
        """
        pass

    def undocumented_method(self):
        pass

    def _private_method(self):
        """Cras tempus lacus nec leo ultrices suscipit."""
        pass
