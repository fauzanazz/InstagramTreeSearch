class StringCompare:
    """
    Compare two strings
    """
    def __init__(self, s1, s2):
        self.count = 0
        self.s1 = s1
        self.s2 = s2

    def compare(self):
        """
        Compare two strings
        :return: bool, True if the strings are equal, False otherwise
        """
        return self.s1 == self.s2

    def substring(self):
        """
        Is s2 a substring of s1
        :return: bool, True if s2 is a substring of s1, False otherwise
        """
        self.count += 1
        is_substring = self.s2 in self.s1
        return is_substring
