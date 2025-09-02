class PhotoStatus:
    PENDING = 'P'
    REJECTED = 'R'
    APPROVED = 'A'
    DELETED = 'D'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (APPROVED, 'Approved'),
        (DELETED, 'Deleted'),
    ]
