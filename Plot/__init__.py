import cairo
import matplotlib.pyplot as pp


class Properties:
    """

    Defines the style of Heatmap plots

    *size* defines the block size.
    *xoff* defines x offset.
    *yoff* defines y offset.

    """

    def __init__(self, size=20, xoff=20, yoff=100):
        self.size = size
        self.xoffset = xoff
        self.yoffset = yoff


class Heatmap:
    """

    This class creates a heatmap object

    :param probes: A list of probes.
    :param samples: A list of groups.
    :param file_name: output filename.
    :param properties: An instance of Properties class `[optional]`.

    :return: writes a PNG image onto disk.

    """

    def __init__(self, samples, probes, file_name, properties=Properties()):

        block_size = properties.size

        w = 150 + len(probes) * block_size
        h = 300 + len(samples) * block_size

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        ctx = cairo.Context(surface)

        # White background
        ctx.rectangle(0, 0, w, h)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()

        x = properties.xoffset  # 10
        y = properties.yoffset  # 100

        x += 90 + block_size / 2
        for probe in probes:
            ctx.save()
            ctx.set_source_rgb(0, 0, 0)
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(10)
            ctx.move_to(x + block_size / 2, y + block_size)
            ctx.rotate(-90)
            ctx.show_text(probe.id)
            ctx.restore()
            x += block_size

        x = properties.xoffset
        y += block_size
        for sample in samples:
            y += block_size
            ctx.set_source_rgb(0, 0, 0)
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(10)
            ctx.move_to(x, y + block_size / 2)
            ctx.show_text(sample.name)
            x += 100
            for probe in probes:
                try:
                    val = sample.probes[probe.id]
                    nan = False
                except Exception as ex:
                    val = 0
                    nan = True
                finally:
                    self.block(ctx, x, y, block_size, val, nan=nan)

                x += block_size
            x = properties.xoffset
        x = 100 + block_size / 2

        y += 10
        for probe in probes:
            ctx.save()
            ctx.set_source_rgb(0, 0, 0)
            ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(10)
            ctx.move_to(x + block_size / 2, y + block_size)
            ctx.rotate(90)
            for i in probe.loc:
                ctx.show_text("%s " % i)

            ctx.restore()
            x += block_size

            # x += 10
        y = 10
        x = 50

        y += block_size * 2
        grad = cairo.LinearGradient(x, y, x + 200.0, y)

        grad.add_color_stop_rgb(0, 1, 0, 0)  # First stop, 50% opacity
        grad.add_color_stop_rgb(1, 1, 1, 1)  # Last stop, 100% opacity

        ctx.move_to(x - 10, y)
        ctx.show_text("1")
        ctx.move_to(x + 200, y)
        ctx.show_text("0")

        ctx.rectangle(x, y, 200, 10)  # Rectangle(x0, y0, x1, y1)
        ctx.set_source(grad)
        ctx.fill()
        ctx.rectangle(x, y, 200, 10)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()

        surface.write_to_png(file_name)

    @staticmethod
    def block(ctx, x, y, size, intensity, nan=False):
        """

        Create a single block. Used by Heatmap class.

        :param ctx: cairo context
        :param x: x-coordinate
        :param y: y-coordinate
        :param size: block size
        :param intensity: color intensity
        :param nan: null value
        :return: Draws a block

        """
        ctx.rectangle(x, y, size, size)
        if not nan:
            ctx.set_source_rgb(1, 1 - intensity, 1 - intensity)
        else:
            ctx.set_source_rgb(0, 0, 0)

        ctx.fill()
        ctx.rectangle(x, y, size, size)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(1)
        ctx.stroke()


class BoxPlot:
    """

    Box plot class creates a BoxPlot figure from probes and groups.


    :param probe_list: A list of probes.
    :param samples: A list of groups.
    :param filename: output filename.
    :param imgtype: output image format.

    :return: writes an image onto disk.

    """

    def __init__(self, probe_list, samples, filename="boxplot", imgtype="png"):
        """

        Create a new BoxPlot.

        :param probe_list: A list of probes.
        :param samples: A list of groups.
        :return:

        """
        self.probe_list = probe_list
        self.samples = samples

        data = []
        for sample in samples:

            sample_data = []
            for probe in self.probe_list:
                try:
                    sample_data.append(sample.probes[probe.id])

                except Exception as ex:
                    pass

            data.append(sample_data)

        samples_name = [sample.name for sample in samples]

        fig, ax1 = pp.subplots(figsize=(10,6))
        fig.canvas.set_window_title("Sample methylation boxplot")
        ax1.set_axisbelow(True)


        ax1.set_ylabel("Beta value")
        ax1.set_xlabel("Sample")
        ax1.yaxis.grid(True, linestyle="-", which= "major", color="lightgrey", alpha=0.5)
        bp= pp.boxplot(data, labels=samples_name, notch=0, sym="+", vert=1, whis=1.5)
        pp.xticks(fontsize=8)
        pp.setp(bp["boxes"], color = "royalblue")
        pp.setp(bp["whiskers"], color = "black")
        pp.setp(bp["fliers"], color = "red", marker="+")
        ax1.set_ylim(-.5, 1.5)

        #pp.show()
        pp.savefig("%s.%s" % (filename, imgtype))


class BoxPlotGroups:
    """

    Box plot class creates a BoxPlot figure from Grouped groups.


    :param probe_list: A list of probes.
    :param groups: A list of groups.
    :param filename: output filename.
    :param imgtype: output image format.

    :return: writes an image onto disk.

    """

    def __init__(self, probe_list, group1, group2, filename="boxplot", imgtype="png"):
        """

        Create a new BoxPlot.

        :param probe_list: A list of probes.
        :param group: A list of group.
        :return:

        """
        self.probe_list = probe_list
        self.group1 = group1
        self.group2 = group2
        data = []
        for sample in group:

            sample_data = []
            for probe in self.probe_list:
                try:
                    sample_data.append(sample.probes[probe.id])

                except Exception as ex:
                    pass

            data.append(sample_data)

        samples_name = [sample.name for sample in group]

        fig, ax1 = pp.subplots(figsize=(10,6))
        fig.canvas.set_window_title("Sample methylation boxplot")
        ax1.set_axisbelow(True)


        ax1.set_ylabel("Beta value")
        ax1.set_xlabel("Sample")
        ax1.yaxis.grid(True, linestyle="-", which= "major", color="lightgrey", alpha=0.5)
        bp= pp.boxplot(data, labels=samples_name, notch=0, sym="+", vert=1, whis=1.5)
        pp.xticks(fontsize=8)
        pp.setp(bp["boxes"], color = "royalblue")
        pp.setp(bp["whiskers"], color = "black")
        pp.setp(bp["fliers"], color = "red", marker="+")
        ax1.set_ylim(-.5, 1.5)

        #pp.show()
        pp.savefig("%s.%s" % (filename, imgtype))
