#include <stdint.h>

struct Shape {
    double x;
    double y;
    double w;
    double h;
};


int draw_frames(uint32_t n, uint8_t px_data[n], uint32_t px_assoc[n], struct Shape px_shape[n], uint32_t img_id[n], struct Shape img_box_lo[n], struct Shape img_box_gl[n], double cam_xy[2], double *cam_z, uint32_t width, uint32 height, uint8_t screen[width][height][3]) {
    const uint8_t N_COLORS = 3;
    uint32_t id = 0;
    double x_lo = 0, y_lo = 0, w_lo = 0, h_lo = 0;
    double x_hi = 0, y_hi = 0, w_hi = 0, h_hi = 0;
    for (uint32_t i = 0; i < n; i++) {
        id = img_id[i];
        // local (lo) and global (gl)
        // column offset (x), row offset (y), column range (w) and row range (h)
        x_lo = img_box_lo[i].x;
        y_lo = img_box_lo[i].y;
        w_lo = img_box_lo[i].w;
        h_lo = img_box_lo[i].h;
        x_gl = img_box_gl[i].x;
        y_gl = img_box_gl[i].y;
        w_gl = img_box_gl[i].w * cam_z;
        h_gl = img_box_gl[i].h * cam_z;
        // cull pixels outside of the screen
        x_screen = (x_gl - cam_xy[0]) * cam_z;
        y_screen = (y_gl - cam_xy[1]) * cam_z;
        x_clip = min(max(x_screen, 0), screen_width);
        y_clip = min(max(y_screen, 0), screen_height);
        w_clip = (uint32_t)(min(max(w_gl + x_screen, 0), screen_width) - x_clip);
        h_clip = (uint32_t)(min(max(h_gl + y_screen, 0), screen_height) - y_clip);

    }

        # scaling factors
        h_fac = (h_lo - 1) / (h_gl - 1)
        w_fac = (w_lo - 1) / (w_gl - 1)
        h_lo_max = px_shape[id][1]

        for y_rel in nb.prange(h_clip):
            for x_rel in range(w_clip):
                for ch in range(OFFSET_RGB):
                    screen[round(x_clip + x_rel), round(y_clip + y_rel), ch] = px_data[
                        px_assoc[id] +
                        (h_lo_max * OFFSET_RGB * round(x_lo + (x_clip - x_screen + x_rel) * w_fac)) +
                        (OFFSET_RGB * round(y_lo + (y_clip - y_screen + y_rel) * h_fac)) +
                        ch
                    ]
    return 0;
}

@cc.export("draw_frames", "void(u1[:], u4[:], u4[:,:], u4, u4[:], f8[:,:], f8[:,:], f8[:], f8, u1[:,:,:], u4, u4)")
def draw_frames(
        px_data: np.array,
        px_assoc: np.array,
        px_shape: np.array,
        img_count: int,
        img_id: np.array,
        img_box_lo: np.array,
        img_box_gl: np.array,
        cam_xy: np.array,
        cam_z: float,
        screen: np.array,
        screen_width: int,
        screen_height: int
):
    OFFSET_RGB = 3
    for i in range(img_count):
        id = img_id[i]

        # local (lo) and global (gl)
        # column offset (x), row offset (y), column range (w) and row range (h)
        x_lo = img_box_lo[i, 0]
        y_lo = img_box_lo[i, 1]
        w_lo = img_box_lo[i, 2]
        h_lo = img_box_lo[i, 3]
        x_gl = img_box_gl[i, 0]
        y_gl = img_box_gl[i, 1]
        w_gl = img_box_gl[i, 2] * cam_z
        h_gl = img_box_gl[i, 3] * cam_z

        # cull pixels outside of the screen
        x_screen = (x_gl - cam_xy[0]) * cam_z
        y_screen = (y_gl - cam_xy[1]) * cam_z
        x_clip = min(max(x_screen, 0), screen_width)
        y_clip = min(max(y_screen, 0), screen_height)
        w_clip = int(min(max(w_gl + x_screen, 0), screen_width) - x_clip)
        h_clip = int(min(max(h_gl + y_screen, 0), screen_height) - y_clip)

        # scaling factors
        h_fac = (h_lo - 1) / (h_gl - 1)
        w_fac = (w_lo - 1) / (w_gl - 1)
        h_lo_max = px_shape[id][1]

        for y_rel in nb.prange(h_clip):
            for x_rel in range(w_clip):
                for ch in range(OFFSET_RGB):
                    screen[round(x_clip + x_rel), round(y_clip + y_rel), ch] = px_data[
                        px_assoc[id] +
                        (h_lo_max * OFFSET_RGB * round(x_lo + (x_clip - x_screen + x_rel) * w_fac)) +
                        (OFFSET_RGB * round(y_lo + (y_clip - y_screen + y_rel) * h_fac)) +
                        ch
                    ]

@cc.export("draw_grid", "void(u1[:], u4, u4, u4, f8[:], f8, u1[:,:,:])")
@nb.jit(nopython=True, parallel=True, fastmath=True)
def draw_grid(
        color: np.array,
        width: int,
        height: int,
        cell_size: int,
        cam_xy: np.array,
        cam_z: float,
        screen: np.array
):
    grid_color = 255 - int(float(color[0] + color[1] + color[2]) / 3)

    start_col = cam_xy[0] - (cam_xy[0] % cell_size)
    start_row = cam_xy[1] - (cam_xy[1] % cell_size)

    n_col = min(int(width / cell_size / cam_z) + 1, width)
    n_row = min(int(height / cell_size / cam_z) + 1, width)

    t = (1 - 1 / (cam_z + 1)) ** 2
    # griglia
    for i in nb.prange(n_col - 1):
        col = int((start_col + (i + 1) * cell_size - cam_xy[0]) * cam_z)
        for row in range(height):
            screen[col, row, 0] = int(t * grid_color + (1-t) * color[0])
            screen[col, row, 1] = int(t * grid_color + (1-t) * color[1])
            screen[col, row, 2] = int(t * grid_color + (1-t) * color[2])

    for j in nb.prange(n_row - 1):
        row = int((start_row + (j + 1) * cell_size - cam_xy[1]) * cam_z)
        for col in range(width):
            screen[col, row, 0] = int(t * grid_color + (1-t) * color[0])
            screen[col, row, 1] = int(t * grid_color + (1-t) * color[1])
            screen[col, row, 2] = int(t * grid_color + (1-t) * color[2])

    # bordi sud-est
    col = int((start_col + n_col * cell_size - cam_xy[0]) * cam_z)
    if col < width:
        for row in range(height):
            screen[col, row, 0] = int(t * grid_color + (1-t) * color[0])
            screen[col, row, 1] = int(t * grid_color + (1-t) * color[1])
            screen[col, row, 2] = int(t * grid_color + (1-t) * color[2])
    
    row = int((start_row + n_row * cell_size - cam_xy[1]) * cam_z)
    if row < height:
        for col in range(width):
            screen[col, row, 0] = int(t * grid_color + (1-t) * color[0])
            screen[col, row, 1] = int(t * grid_color + (1-t) * color[1])
            screen[col, row, 2] = int(t * grid_color + (1-t) * color[2])


if __name__ == "__main__":
    cc.compile()
