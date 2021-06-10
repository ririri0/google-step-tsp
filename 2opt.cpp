#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <list>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

typedef struct {
  double x;
  double y;
} xy;

std::vector<xy> load_csv(int num) {
  std::vector<xy> dist_data;

  // input
  std::string str_buf;
  std::string input_file_path = "input_" + std::to_string(num) + ".csv";
  std::ifstream ifs_file(input_file_path);

  // "index"
  getline(ifs_file, str_buf);

  // x, y
  while (getline(ifs_file, str_buf)) {
    int divided_index = str_buf.find(',');
    double x = std::stod(str_buf.substr(0, divided_index));
    double y = std::stod(str_buf.substr(divided_index + 1));
    // Create Data
    xy push_data = {x, y};
    dist_data.push_back(push_data);
  }

  ifs_file.close();
  return dist_data;
}

void output_data(int num, std::vector<int> tour) {
  std::string output_file_path = "output_" + std::to_string(num) + ".csv";
  std::ofstream ofs_file(output_file_path);

  ofs_file << "index" << std::endl;
  for (int i = 0; i < tour.size(); i++) {
    ofs_file << tour[i] << std::endl;
  }
  ofs_file.close();
}

double distance(xy xy1, xy xy2) {
  // ルートは省略
  return ((xy1.x - xy2.x) * (xy1.x - xy2.x)) +
         ((xy1.y - xy2.y) * (xy1.y - xy2.y));
}

int serach_next_city(int N, std::vector<bool> unvisited_cities, double *dist,
                     int current_index) {
  int min_index = -1;
  double min_dist = 4000000.0;

  // for (int i = 0; i < unvisited_cities.size(); i++) {
  // std::cout << unvisited_cities[i] << endl;
  //}

  for (int i = 0; i < N; i++) {
    std::cout << boolalpha << unvisited_cities[i] << " " << i << " "
              << current_index << "\n";
    std::cout << current_index << " ";

    if (dist[current_index * N + i] < min_dist) {
      if (unvisited_cities[i] && current_index != i) {
        min_index = i;
        min_dist = dist[current_index * N + i];
      }
    }
  }

  if (min_index == -1) {
    exit(1);
  } else {
    return min_index;
  }
}

double total_distance(int N, std::vector<int> tour, double *dist) {
  double total = 0;
  for (int i = 0; i < N; i++) {
    int index1 = tour[i];
    int index2 = tour[i + 1];
    total += dist[index1 * N + index2];
  }
  total += dist[tour[0] * N + tour[tour.size() - 1]];
  return total;
}

std::vector<int> solve_greedy_all_start_index(std::vector<xy> location_data, double *dist) {
  int N = location_data.size();
  int current_index;

  int min_total_dist = 4000000;
  std::vector<int> min_tour(N);
  for (int start_index = 0; start_index < 1; start_index++) {
    current_index = start_index;
    std::vector<int> tour;
    // Search
    tour.push_back(current_index);
    std::vector<bool> unvisited_cities(N, true);

    while (tour.size() < N) {
      int next_index =
          serach_next_city(N, unvisited_cities, dist, current_index);
      tour.push_back(next_index);
      unvisited_cities[next_index] = false;
      current_index = next_index;
    }

    for (int univ_num = 0; univ_num < unvisited_cities.size(); univ_num++) {
      if (unvisited_cities[univ_num] == false) {
        tour.push_back(univ_num);
      }
    }

    // Compare
    double total_dist = total_distance(N, tour, dist);
    if (total_dist < min_total_dist) {
      min_total_dist = total_dist;
      std::copy(tour.begin(), tour.end(), min_tour.begin());
    }
  }
  // free(dist);
  return min_tour;
}

int main() {
  for (int i = 0; i < 6; i++) {
    // Input
    std::vector<xy> data = load_csv(i);
    // Calculation
    double *dist = (double *)malloc(N * N * sizeof(double));
    ;

    for (int i = 0; i < N; i++) {
      for (int j = i; j < N; j++) {
        dist[i * N + j] = dist[j * N + i] =
            distance(location_data[i], location_data[j]);
      }
    }
    std::vector<int> tour = solve_greedy_all_start_index(data, dist);
    // Output
    output_data(i, tour);
  }
}
