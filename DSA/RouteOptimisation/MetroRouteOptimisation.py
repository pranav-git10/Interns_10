from collections import defaultdict, deque
import heapq


class MetroGraph:
    """
    A graph representation of a metro system with pathfinding capabilities.
    Supports Dijkstra's algorithm, BFS, and DFS for finding routes between stations.
    """
    
    def __init__(self):
        self._adjacency_list: dict[str, dict[str, int]] = defaultdict(dict)
    
    def add_connection(self, station1: str, station2: str, travel_time: int) -> None:
        """Add a bidirectional connection between two stations."""
        self._adjacency_list[station1][station2] = travel_time
        self._adjacency_list[station2][station1] = travel_time
    
    def _validate_stations(self, source: str, destination: str) -> bool:
        """Check if both stations exist in the network."""
        return source in self._adjacency_list and destination in self._adjacency_list
    
    def _reconstruct_path(self, predecessors: dict[str, str], destination: str) -> list[str]:
        """Reconstruct path from predecessors dictionary."""
        path = []
        current = destination
        
        while current:
            path.append(current)
            current = predecessors.get(current)
        
        return path[::-1]  # Reverse to get source -> destination order
    
    def find_shortest_path(self, source: str, destination: str) -> list[str]:
        """
        Find the shortest path using Dijkstra's algorithm.
        Returns None if no path exists or invalid stations.
        """
        if not self._validate_stations(source, destination):
            return None
        
        if source == destination:
            return [source]
        
        distances = defaultdict(lambda: float('inf'))
        distances[source] = 0
        predecessors = {}
        priority_queue = [(0, source)]
        visited = set()
        
        while priority_queue:
            current_distance, current_station = heapq.heappop(priority_queue)
            
            if current_station in visited:
                continue
            
            visited.add(current_station)
            
            if current_station == destination:
                return self._reconstruct_path(predecessors, destination)
            
            for neighbor, travel_time in self._adjacency_list[current_station].items():
                if neighbor not in visited:
                    new_distance = current_distance + travel_time
                    
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = current_station
                        heapq.heappush(priority_queue, (new_distance, neighbor))
        
        return None  # No path found
    
    def find_path_bfs(self, source: str, destination: str) -> list[str]:
        """
        Find any path using BFS (shortest in terms of number of stations).
        Returns None if no path exists or invalid stations.
        """
        if not self._validate_stations(source, destination):
            return None
        
        if source == destination:
            return [source]
        
        visited = {source}
        predecessors = {}
        queue = deque([source])
        
        while queue:
            current_station = queue.popleft()
            
            for neighbor in self._adjacency_list[current_station]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    predecessors[neighbor] = current_station
                    queue.append(neighbor)
                    
                    if neighbor == destination:
                        return self._reconstruct_path(predecessors, destination)
        
        return None  # No path found
    
    def find_path_dfs(self, source: str, destination: str) -> list[str]:
        """
        Find any path using DFS.
        Returns None if no path exists or invalid stations.
        """
        if not self._validate_stations(source, destination):
            return None
        
        if source == destination:
            return [source]
        
        def dfs_recursive(current: str, target: str, visited: set[str], path: list[str]) -> bool:
            visited.add(current)
            path.append(current)
            
            if current == target:
                return True
            
            for neighbor in self._adjacency_list[current]:
                if neighbor not in visited:
                    if dfs_recursive(neighbor, target, visited, path):
                        return True
            
            path.pop()  # Backtrack
            visited.remove(current)
            return False
        
        visited = set()
        path = []
        
        if dfs_recursive(source, destination, visited, path):
            return path
        
        return None  # No path found
    
    def calculate_travel_time(self, path: list[str]) -> int:
        """Calculate total travel time for a given path."""
        if len(path) < 2:
            return 0
        
        return sum(
            self._adjacency_list[path[i]][path[i + 1]]
            for i in range(len(path) - 1)
        )
    
    def get_stations(self) -> list[str]:
        return list(self._adjacency_list.keys())


class MetroPathfinder:
    """Main application class for metro pathfinding."""
    
    ALGORITHMS = {
        1: ("Dijkstra (Shortest Time)", "find_shortest_path"),
        2: ("BFS (Fewest Stops)", "find_path_bfs"),
        3: ("DFS (Any Path)", "find_path_dfs")
    }
    
    def __init__(self):
        self.metro = MetroGraph()
        self._setup_network()
    
    def _setup_network(self) -> None:
        """Initialize the metro network with predefined connections."""
        connections = [
            ("A", "B", 5),
            ("A", "C", 10),
            ("B", "C", 2),
            ("B", "D", 3),
            ("C", "D", 1),
            ("C", "E", 7),
            ("D", "E", 4)
        ]
        
        for station1, station2, time in connections:
            self.metro.add_connection(station1, station2, time)
    
    def _get_user_input(self) -> tuple[str, str, int]:
        """Get source, destination, and algorithm choice from user."""
        print(f"Available stations: {', '.join(sorted(self.metro.get_stations()))}")
        
        source = input("Enter source station: ").strip().upper()
        destination = input("Enter destination station: ").strip().upper()
        
        print("\nAvailable algorithms:")
        for key, (name, _) in self.ALGORITHMS.items():
            print(f"{key}. {name}")
        
        while True:
            try:
                choice = int(input("Choose algorithm (1-3): "))
                if choice in self.ALGORITHMS:
                    return source, destination, choice
                print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Please enter a valid number.")
    
    def run(self) -> None:
        """Main application loop."""
        print("=== Metro Pathfinding System ===\n")
        
        source, destination, algorithm_choice = self._get_user_input()
        
        # Get the appropriate method
        _, method_name = self.ALGORITHMS[algorithm_choice]
        find_path_method = getattr(self.metro, method_name)
        
        # Find the path
        path = find_path_method(source, destination)
        
        if path:
            travel_time = self.metro.calculate_travel_time(path)
            print(f"\n✓ Path found: {' → '.join(path)}")
            print(f"✓ Total travel time: {travel_time} minutes")
            print(f"✓ Number of stops: {len(path) - 1}")
        else:
            print(f"\n✗ No path found between '{source}' and '{destination}'")
            print("Please check that both stations exist in the network.")


def main():
    """Entry point of the application."""
    pathfinder = MetroPathfinder()
    pathfinder.run()


if __name__ == "__main__":
    main()