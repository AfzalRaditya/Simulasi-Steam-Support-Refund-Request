import mesa
import random

def compute_avg_frustration(model):
    """Menghitung rata-rata tingkat frustrasi dari semua tiket yang ada."""
    tickets = [a for a in model.agent_list if isinstance(a, TicketAgent)]
    if len(tickets) == 0:
        return 0
    return sum([t.frustration for t in tickets]) / len(tickets)

class TicketAgent(mesa.Agent):
    """Agen tiket refund yang memiliki atribut psikologis (Tingkat Frustrasi)."""
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.unique_id = unique_id
        
        self.playtime = random.uniform(0, 5) 
        self.ownership_days = random.randint(1, 30) 
        self.complexity = random.randint(1, 5) 
        self.status = "Generated"
        self.wait_time = 0
        
        self.frustration = 0.0 
        self.impatience_factor = random.uniform(0.01, 0.05) 
    def step(self):
        if self.status == "In Queue":
            self.wait_time += 1
            self.frustration = min(1.0, self.frustration + self.impatience_factor)

class StaffAgent(mesa.Agent):
    """Agen staf Steam Support."""
    def __init__(self, unique_id, model):
        super().__init__(model)
        self.unique_id = unique_id
        self.status = "Idle"
        self.current_ticket = None
        self.time_spent = 0
        self.processing_rate = 1

    def step(self):
        if self.status == "Busy" and self.current_ticket is not None:
            self.time_spent += self.processing_rate
            if self.time_spent >= self.current_ticket.complexity:
                self.current_ticket.status = "Resolved"
                self.model.resolved_tickets += 1
                self.status = "Idle"
                self.current_ticket = None
                self.time_spent = 0

class SteamSupportModel(mesa.Model):
    """Lingkungan simulasi sistem antrean Steam Support."""
    def __init__(self, base_staff=3, auto_approval=False, dynamic_staffing=False, q_threshold=10, extra_staff=2, max_arrival=4):
        super().__init__()
        self.num_base_staff = base_staff
        self.auto_approval = auto_approval
        self.dynamic_staffing = dynamic_staffing
        self.q_threshold = q_threshold
        self.extra_staff = extra_staff
        self.max_arrival = max_arrival
        
        self.agent_list = []
        self.ticket_queue = []
        self.resolved_tickets = 0
        self.current_id = 0
        
        for _ in range(self.num_base_staff):
            self.add_staff()
            
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Panjang_Antrean": lambda m: len(m.ticket_queue),
                "Tiket_Selesai": "resolved_tickets",
                "Total_Staf": lambda m: len([a for a in m.agent_list if isinstance(a, StaffAgent)]),
                "Rata_Rata_Frustrasi": compute_avg_frustration 
            }
        )

    def add_staff(self):
        staff = StaffAgent(self.current_id, self)
        self.agent_list.append(staff) 
        self.current_id += 1

    def step(self):
        num_new_tickets = random.randint(0, self.max_arrival)
        for _ in range(num_new_tickets):
            ticket = TicketAgent(self.current_id, self)
            self.agent_list.append(ticket) 
            self.current_id += 1
            
            if self.auto_approval and ticket.playtime < 2.0 and ticket.ownership_days < 14:
                ticket.status = "Resolved"
                self.resolved_tickets += 1
            else:
                ticket.status = "In Queue"
                self.ticket_queue.append(ticket)
                
        active_staff_count = len([a for a in self.agent_list if isinstance(a, StaffAgent)])
        if self.dynamic_staffing:
            if len(self.ticket_queue) >= self.q_threshold and active_staff_count == self.num_base_staff:
                for _ in range(self.extra_staff):
                    self.add_staff()
                    
        idle_staff = [a for a in self.agent_list if isinstance(a, StaffAgent) and a.status == "Idle"]
        for staff in idle_staff:
            if len(self.ticket_queue) > 0:
                ticket_to_process = self.ticket_queue.pop(0)
                ticket_to_process.status = "Under Review"
                staff.current_ticket = ticket_to_process
                staff.status = "Busy"
        
        random.shuffle(self.agent_list)
        for agent in self.agent_list:
            agent.step()
            
        self.datacollector.collect(self)