#include <bits/stdc++.h>

using namespace std;

const int seed_h = 109202;
const int seed_b = 477828;
const int qual = 300;
const double lim = 28;
const double heigh = 30;
vector <double> variate = {1, 1, 0.9, 0.98};
vector <double> friction = {1, 1, 1, 1};
const int rad = 10000;
int p_size = 500;
double var_h = 100;
double a_size = M_PI * 0.6;
double k_step = 0.004;
tuple <double, double, double> field[500][500]; // ïîëå, îïðåäåëÿþùåå ðàçíîñòü äàâëåíèé
double mod(long long x, long long y) {
    return sqrt(x * x + y * y) + 0.1;
}

double f1(double x) {
    return max(((x+0.3) * (1 - (x+0.3)/1.3) + 0.1) * 3, (double) 0);
}

double f2(double x) {
    if (x < 1) {
        return (double) 1;
    }
    else {
        return (double) 0;
    }
}

double f3(double x) {
    return sqrt(x);
}

double rand_v(int x, int y, int seed) {

    x %= 1000000007;
    y %= 1000000009;

    int pre = y * (seed - y) * (2 * seed - y) + x * (seed - x) * (2 * seed - x) - pow(x + y, 3);
    pre %= qual;
    return ((double) pre) / qual * 2 * M_PI;
}

double val(long long x, long long y, int seed) {

    int x_int = x / qual;
    int y_int = y / qual;

    x %= qual;
    y %= qual;

    double xd = (double) x / qual;
    double yd = (double) y / qual;

    vector <pair <int, int>> mv = {{0, 0}, {0, 1}, {1, 0}, {1, 1}};

    double value = 0;
    double mas = 0;

    for (auto i : mv) {
        double ang = rand_v(x_int + i.first, y_int + i.second, seed);
        double x1 = xd - i.first;
        double y1 = yd - i.second;

        double len = x1 * x1 + y1 * y1 + 0.001;
        len = sqrt(len);

        double m = max(1 / len / len - 1, (double) 0);

        value += (cos(ang) * x1 + sin(ang) * y1 + 0.001) * m;
        mas += m;
    }

    return value / mas;

}

double val_h(long long x, long long y, int seed) {
    //return 0; // äåôîëò ïóñòîãî ïîëÿ
    double value_h = 0;
    for (int i = 0; i < 8; i++) { // äåáàã (i < 8)
        value_h += val((int) (x / pow(2, i)), (int) (y / pow(2, i)), seed) * pow(1.6, i) * var_h;
    }
    return value_h;
}


pair <double, double> grad_h(long long x, long long y, int seed) {
    return {val_h(x + 1, y, seed) - val_h(x, y, seed), val_h(x, y + 1, seed) - val_h(x, y, seed)};
}


int val_b(long long x, long long y, int seed) {
    vector <double> a = {0, 0.5, 1};
    int cnt = 0;
    double vh = val_h(x, y, seed_h);
    double vb = val_h(x, y, seed_b);
    for (int i = 0; i < a.size() and atan(vh) / M_PI + vb / lim > a[i]; i++) {
        cnt++;
    }
    return cnt;
}

/*
pair <int, double> Ray(long long x, long long y, double ang, double alpha) {
    double len = 0;
    double vh = val_h(x, y, seed_h);
    while (len < rad and val_h(x + len * cos(ang), y + len * sin(ang), seed_h) < vh + heigh + len * alpha){
        len += (vh + len * alpha + heigh - val_h(x + len * cos(ang), y + len * sin(ang), seed_h)) * k_step * (len + 333) * cos(alpha) + 5;
    }
    len = len / cos(alpha);
    if (len < rad) {
        return {val_b(x + (long long)(len * cos(ang)), y + (long long)(len * sin(ang)), seed_b), len};
    }
    else {
        return {-1, rad};
    }
}*/


pair <int, double> Ray(long long x, long long y, double ang, double alpha, double start_len) {
    double len = start_len; // default - 50
    double vh = val_h(x, y, seed_h);
    double help;
    double last_len = 0;
    double last_h = vh;
    double ans;
    double last_ans = heigh;
    while (len < rad and (ans = ((help = val_h(x + len * cos(ang), y + len * sin(ang), seed_h)) - (vh + heigh + len * alpha))) < 0){
        last_len = len;
        len += (vh + len * alpha + heigh - help + 10) * k_step * (len + 200) * cos(alpha) + 5;
        last_h = help;
        last_ans = ans;
    }
    len = (abs(last_len * ans) + abs(len * last_ans)) / (abs(ans) + abs(last_ans));
    len = len / cos(alpha);
    if (len < rad) {
        return {val_b(x + (long long)(len * cos(ang)), y + (long long)(len * sin(ang)), seed_b), len};
    }
    else {
        return {-1, rad};
    }
}


struct Spider {

    double ang;
    pair <double, double> focus = {0, 0};
    double focus_len = 1; // íàñòðîèòü ôîêóñ
    pair <long long, long long> coords = {0, 0};
    pair <double, double> move_v = {0, 0};
    vector <bool> got;
    vector <double> lens;
    vector <double> power;
    vector <pair <long long, long long>> points;

    Spider() {
        coords = {10000, 10000};
        move_v = {0, 0};
        ang = M_PI * 0;
        points = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        got.assign(4, 0);
        power.assign(4, 0);
        lens.assign(4, 1);

    }

    void act() {

        long long dx1, dx2, dy1, dy2;
        dx1 = points[3].first - coords.first;
        dy1 = points[3].second - coords.second;
        dx2 = points[0].first - coords.first;
        dy2 = points[0].second - coords.second;

        double ang_3, ang_0;

        ang_3 = acos(dx1 / mod(dx1, dy1));
        ang_0 = acos(dx1 / mod(dx1, dy1));
        double pre_ang = (ang_3 + ang_0) / 2;

        if (ang_3 > ang_3) {
            ang += M_PI;
        }
        if (ang >= M_PI * 2) {
            ang -= M_PI * 2;
        }

        if (sin(ang_3) != dy1 / mod(dx1, dy1)) {
            ang_3 = -ang_3;
        }

        if (sin(ang_3) != dy1 / mod(dx1, dy1)) {
            ang_3 = -ang_3;
        }

        for (int i = 0; i < 4; i++) {
            if (friction[val_b(points[i].first, points[i].second, seed_b)] < power[i]) {
                got[i] = 0;
            }
            if (got[i] == 0) {
                lens[i] -= power[i];
            }
            else {
                double dx = points[i].first - move_v.first;
                double dy = points[i].second - move_v.second;
                move_v.first += dx * power[i] / mod(dx, dy);
                move_v.second += dy * power[i] / mod(dx, dy);
            }
        }
        coords.first += (long long) move_v.first;
        coords.second += (long long) move_v.second;
        for (int i = 0; i < 4; i++) {
            lens[i] = mod(points[i].first - coords.first, points[i].second - coords.second);
        }
    }

    void get(int ind) {
        if (got[ind] == 1 or val_h(coords.first, coords.second, seed_h) < 0) {
            return;
        }
        else {
            points[ind] = {coords.first + (long long) (cos(ang + M_PI / 4 + M_PI * ind / 2) * lens[ind]), coords.second + (long long) (sin(ang + M_PI / 4 + M_PI * ind / 2) * lens[ind])};
        }
    }

    void pict(vector <vector <pair <int, double>>> &ans) {

        pair <double, double> gr = grad_h(coords.first, coords.second, seed_h);

        double scal = (gr.first * cos(ang) + gr.second * sin(ang));

        for (double i_p = 0; i_p < p_size; i_p++) {
            double len_start = 50;
            for (double j_p = 0; j_p < p_size; j_p++) {

                double i, j;
                double ln = f3(mod(i_p - 0.5 * p_size, j_p - 0.5 * p_size) / p_size);
                ln = 1; // äåáàã íà óñêîðåíèå
                i = (int) (0.5 * p_size + (i_p - 0.5 * p_size) * ln);
                j = (int) (0.5 * p_size + (j_p - 0.5 * p_size) * ln);


                double ang1 = ang - a_size / 2 + i * a_size / p_size;
                double ang2 = a_size / 2 - j * a_size / p_size + scal / sqrt(2); // èçìåíÿþùèé ôîêóñ
                ans[i_p][j_p] = Ray(coords.first, coords.second, ang1, sin(ang2), len_start);
                len_start = max(ans[i_p][j_p].second * 0.9, (double) 50);
            }
        }
    }
};


int main() {

    setprecision(10);

    int a = 500;
    long long start_x = 500;
    long long start_y = 0;
    long long zoom = 100;

    Spider sp;

    freopen("spider6.txt", "w", stdout);

    vector <vector <pair <int, double>>> picture(p_size, vector <pair <int, double>>(p_size));

    sp.pict(picture);

    for (int i = 0; i < p_size; i++) {
        for (int j = 0; j < p_size; j++) {
            cout << (int) picture[i][j].second << " ";
        }
        cout << endl;
    }


    return 0;
}
