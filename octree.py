import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button, RadioButtons
import random
import numpy as np 

# --- PARTE 1: Estrutura de Dados do Octree ---

class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

class AABB:
    def __init__(self, center, half_dimension):
        self.center = center
        self.half = half_dimension

    def contains(self, point):
        return (self.center.x - self.half <= point.x < self.center.x + self.half and
                self.center.y - self.half <= point.y < self.center.y + self.half and
                self.center.z - self.half <= point.z < self.center.z + self.half)

class Octree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.children = []

    def subdivide(self):
        x, y, z = self.boundary.center.x, self.boundary.center.y, self.boundary.center.z
        h = self.boundary.half / 2
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                for dz in [-1, 1]:
                    new_center = Point(x + dx*h, y + dy*h, z + dz*h)
                    self.children.append(Octree(AABB(new_center, h), self.capacity))
        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point): return False
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            return True
        if not self.divided:
            self.subdivide()
            for p in self.points:
                for child in self.children:
                    if child.insert(p): break
            self.points = []
        for child in self.children:
            if child.insert(point): return True
        return False

# --- PARTE 2: Geradores de Formas ---

def gerar_aleatorio(num_points, domain_size):
    points_data = []
    for _ in range(num_points):
        x = random.uniform(-domain_size/2, domain_size/2)
        y = random.uniform(-domain_size/2, domain_size/2)
        z = random.uniform(-domain_size/2, domain_size/2)
        points_data.append([x, y, z])
    return points_data

def gerar_flor(num_points, scale=80):
    points_data = []
    thetas = np.linspace(0, 2*np.pi, num_points)
    for theta in thetas:
        k = 4 
        r = np.cos(k * theta) * scale
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        z = random.uniform(-15, 15) # Z um pouco maior para dar volume
        # Adiciona ruído
        x += random.uniform(-5, 5)
        y += random.uniform(-5, 5)
        points_data.append([x, y, z])
    return points_data

def gerar_rosquinha(num_points, R=60, r=25):
    """
    Gera pontos na forma de um Torus (Rosquinha).
    R = Raio maior (distância do centro do furo até o centro do tubo)
    r = Raio menor (espessura do tubo)
    """
    points_data = []
    for _ in range(num_points):
        # Ângulos aleatórios
        theta = random.uniform(0, 2 * np.pi) # Ângulo ao redor do tubo
        phi = random.uniform(0, 2 * np.pi)   # Ângulo ao redor do centro do Torus
        
        # Matemática do Torus
        x = (R + r * np.cos(theta)) * np.cos(phi)
        y = (R + r * np.cos(theta)) * np.sin(phi)
        z = r * np.sin(theta)
        
        points_data.append([x, y, z])
    return points_data

# --- PARTE 3: Visualização ---

def draw_aabb(ax, aabb):
    x, y, z = aabb.center.x, aabb.center.y, aabb.center.z
    h = aabb.half
    vertices = [[x-h, y-h, z-h], [x+h, y-h, z-h], [x+h, y+h, z-h], [x-h, y+h, z-h], [x-h, y-h, z+h], [x+h, y-h, z+h], [x+h, y+h, z+h], [x-h, y+h, z+h]]
    edges = [[0,1], [1,2], [2,3], [3,0], [4,5], [5,6], [6,7], [7,4], [0,4], [1,5], [2,6], [3,7]]
    for edge in edges:
        p1, p2 = vertices[edge[0]], vertices[edge[1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='black', linewidth=0.5, alpha=0.2)

def visualize_octree(octree, ax):
    if octree.points or octree.divided:
         draw_aabb(ax, octree.boundary)
    if octree.divided:
        for child in octree.children:
            visualize_octree(child, ax)

# --- PARTE 4: Interface Gráfica ---

def main():
    fig = plt.figure(figsize=(12, 8))
    plt.subplots_adjust(left=0.3, bottom=0.1) 
    
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("Selecione uma forma e clique em 'Gerar'")
    ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')

    domain_size = 250
    
    # Widgets
    ax_radio = plt.axes([0.05, 0.4, 0.15, 0.25], facecolor='lightgoldenrodyellow')
    ax_btn_start = plt.axes([0.05, 0.25, 0.15, 0.075])
    ax_btn_quit = plt.axes([0.05, 0.15, 0.15, 0.075])

    radio_options = RadioButtons(ax_radio, ('Aleatorio', 'Flor', 'Rosquinha'))
    btn_start = Button(ax_btn_start, 'Gerar', color='lightblue', hovercolor='0.975')
    btn_quit = Button(ax_btn_quit, 'Sair', color='salmon', hovercolor='red')

    def iniciar_simulacao(event):
        ax.clear()
        escolha = radio_options.value_selected
        ax.set_title(f"Visualizacao Octree: {escolha}")
        ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
        
        limit = domain_size / 2
        ax.set_xlim(-limit, limit); ax.set_ylim(-limit, limit); ax.set_zlim(-limit, limit)

        points_data = []
        # Aumentei um pouco os pontos para a rosquinha ficar mais definida
        total_points = 400 

        if escolha == 'Aleatorio':
             points_data = gerar_aleatorio(200, domain_size) # Menos pontos pro aleatório
        elif escolha == 'Flor':
             points_data = gerar_flor(total_points, scale=100)
        elif escolha == 'Rosquinha':
             points_data = gerar_rosquinha(total_points * 2) # Mais pontos pra rosquinha ficar bonita

        # Criar Octree
        center = Point(0, 0, 0)
        boundary = AABB(center, domain_size)
        tree = Octree(boundary, capacity=4) 
        
        for p_arr in points_data:
            tree.insert(Point(p_arr[0], p_arr[1], p_arr[2]))

        # Desenhar Pontos
        px = [p[0] for p in points_data]
        py = [p[1] for p in points_data]
        pz = [p[2] for p in points_data]
        ax.scatter(px, py, pz, c='red', marker='o', s=10, alpha=0.5) 

        # Desenhar Octree
        visualize_octree(tree, ax)
        plt.draw()

    def encerrar(event):
        plt.close(fig)

    btn_start.on_clicked(iniciar_simulacao)
    btn_quit.on_clicked(encerrar)
    plt.show()

if __name__ == "__main__":
    main()