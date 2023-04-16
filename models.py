class CollisionReport:
    def __init__(self, insurance_id, report_id, type_severity_of_collision, injuries, vehicles_involved, damage_to_customers_car, location_of_damage, witnesses, police_called, car_is_drivable):
        self.insurance_id = insurance_id
        self.report_id = report_id
        self.type_severity_of_collision = type_severity_of_collision
        self.injuries = injuries
        self.vehicles_involved = vehicles_involved
        self.damage_to_customers_car = damage_to_customers_car
        self.location_of_damage = location_of_damage
        self.witnesses = witnesses
        self.police_called = police_called
        self.car_is_drivable = car_is_drivable