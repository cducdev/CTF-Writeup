#include <algorithm>
#include <array>
#include <vector>

namespace bfsBot {
    using namespace std;
    const int boardSize = 25, cellCount = boardSize * boardSize;
    const int dx[] = {0, 1, 0, -1};
    const int dy[] = {-1, 0, 1, 0};

    int cellId(int x, int y) {
        return y * boardSize + x;
    };

    int turn(int dir, int action) {
        if (action == 1) return (dir + 3) % 4;
        if (action == 2) return (dir + 1) % 4;
        return dir;
    };

    int step(int cell, int dir) {
        int x = cell % boardSize + dx[dir], y = cell / boardSize + dy[dir];
        if (x < 0 || x >= boardSize || y < 0 || y >= boardSize) return -1;
        return cellId(x, y);
    };

    void bfs(int start, const bool blocked[], int dist[]) {
        fill(dist, dist + cellCount, -1);
        int q[cellCount], first = 0, last = 0;
        q[last++] = start;
        dist[start] = 0;
        while (first < last) {
            int u = q[first++];
            for (int d = 0; d < 4; d++) {
                int v = step(u, d);
                if (v < 0 || blocked[v] || dist[v] != -1) continue;
                dist[v] = dist[u] + 1;
                q[last++] = v;
            };
        };
    };

    struct Bot {
        vector<int> body[2];
        int dir[2] = {};
        int lastAction = 0;
        bool apples[cellCount] = {};
        bool ready = false;

        void observe(const State& state) {
            if (!ready || !state.last_opponent_action) {
                body[0].clear();
                body[1].clear();

                for (auto p : state.initial_self_body) body[0].push_back(cellId(p.x, p.y));
                for (auto p : state.initial_opponent_body) body[1].push_back(cellId(p.x, p.y));

                for (int p = 0; p < 2; p++) {
                    dir[p] = 0;
                    if (body[p].size() < 2) continue;
                    for (int d = 0; d < 4; d++)
                        if (step(body[p][1], d) == body[p][0]) dir[p] = d;
                };

                ready = true;
            } else {
                int actions[] = {lastAction, *state.last_opponent_action};
                for (int p = 0; p < 2; p++) {
                    dir[p] = turn(dir[p], actions[p]);
                    int head = step(body[p][0], dir[p]);
                    if (!apples[head]) body[p].pop_back();
                    body[p].insert(body[p].begin(), head);
                };
            };

            fill(apples, apples + cellCount, false);
            for (auto p : state.apples) apples[cellId(p.x, p.y)] = true;
        };

        int choose(const State& state) {
            observe(state);

            bool occupied[cellCount] = {};
            bool danger[cellCount] = {};

            for (int p = 0; p < 2; p++)
                for (int cell : body[p]) occupied[cell] = true;
            for (int a = 0; a < 3; a++) {
                int v = step(body[1][0], turn(dir[1], a));
                if (v >= 0 && !occupied[v]) danger[v] = true;
            };

            int answer = 0;
            array<int, 6> best = {};
            bool found = false;
            for (int a = 0; a < 3; a++) {
                int head = step(body[0][0], turn(dir[0], a));

                if (head < 0 || occupied[head]) continue;

                bool blocked[cellCount];
                copy(occupied, occupied + cellCount, blocked);
                bool grow = apples[head];
                if (!grow) blocked[body[0].back()] = false;
                blocked[head] = true;

                int mine[cellCount];
                bfs(head, blocked, mine);

                int area = 0, exits = 0, food = cellCount;
                for (int v = 0; v < cellCount; v++) {
                    if (mine[v] >= 0) area++;
                    if (!apples[v] || v == head || mine[v] < 0) continue;
                    food = min(food, mine[v]);
                };
                for (int d = 0; d < 4; d++) {
                    int v = step(head, d);
                    if (v >= 0 && !blocked[v] && !danger[v]) exits++;
                };

                int length = int(body[0].size()) + grow;

                array<int, 6> score = {!danger[head], exits > 0, min(area - length, 0), grow, -food, area};

                if (!found || score > best) {
                    found = true;
                    best = score;
                    answer = a;
                };
            };

            lastAction = answer;
            return answer;
        };
    };
};  // namespace bfsBot

int decide(const State& state) {
    static bfsBot::Bot bot;
    return bot.choose(state);
};
