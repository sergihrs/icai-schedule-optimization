import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class Displayer:
    def __init__(self, tensor, subject_names):
        self.tensor = tensor
        self.groups = ["IMAT-1A", "IMAT-1B", "IMAT-2A", "IMAT-2B", "IMAT-3A"]
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.hours = [
            "8:00",
            "9:00",
            "10:00",
            "11:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00",
            "19:00",
            "20:00",
        ]
        self.subjects_name = subject_names
        self.timetables = {
            group: {day: {hour: [] for hour in self.hours} for day in self.days}
            for group in self.groups
        }
        self.make_dictionary()

    def make_dictionary(self):
        # Populate timetables with subjects and teachers
        for key in self.tensor.keys():
            group, day_index, hour_index, subject, teacher = eval(
                key
            )  # Convert string tuple to actual tuple

            if group in self.groups:
                day = self.days[int(day_index) - 1]
                hour = self.hours[int(hour_index) - 1]

                self.timetables[group][day][hour].append(
                    (subjects_name[subject], teacher)
                )

    def print_terminal(self):
        # Print the timetables
        for group, timetable in self.timetables.items():
            print(f"\nTimetable for {group}:")
            for day, hours_data in timetable.items():
                print(f"\n{day}:")
                for hour, subjects_teachers in hours_data.items():
                    if subjects_teachers:
                        print(f"{hour}: {subjects_teachers}")

    def _to_dataframe(self, group="IMAT-1A"):
        df = pd.DataFrame(
            columns=["Hours", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            index=self.hours,
        )

        for day in self.days:
            for hour in self.hours:
                subject, teacher = (
                    (
                        self.timetables[group][day][hour][0][0],
                        self.timetables[group][day][hour][0][1],
                    )
                    if self.timetables[group][day][hour]
                    else ("", "")
                )
                i = 0
                for char in teacher:
                    if char.isupper() and i > 0:
                        teacher = teacher[:i] + " " + teacher[i:]
                        i += 1
                    i += 1

                df.loc[hour, day] = f"{subject}\n\n{teacher}"

        df["Hours"] = self.hours
        df = df.rename(columns={"Hours": ""})

        df = df.replace("\n\n", None).dropna(how="all", subset=self.days).fillna("")

        return df

    def print_pdf(self, group="IMAT-1A", output_file="docs/timetable.pdf"):
        df = self._to_dataframe(group)

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.axis("tight")
        ax.axis("off")

        # Create a table and add it to the figure
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            cellLoc="center",
            loc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(4)

        for key in table._cells:
            if key[0] == 0:
                # make the text bold
                table._cells[key].set_text_props(weight="bold")
                continue
            if key[1] == 0:
                table._cells[key].set_text_props(weight="bold")
            cell = table._cells[key]
            cell.set_height(0.07)  # You can adjust this value based on your preference

        # Save the figure to a PDF
        with PdfPages(output_file) as pdf:
            # Save the figure to the PDF next to the title
            pdf.savefig(fig, bbox_inches="tight", pad_inches=0)

        plt.close()


if __name__ == "__main__":
    with open("assets/schedules.json") as json_file:
        tensor = json.load(json_file)

    with open("data/subject-name.json") as json_file:
        subjects_name = json.load(json_file)

    displayer = Displayer(tensor, subjects_name)
    displayer.print_pdf()
