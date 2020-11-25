package me.mpoc.fixkclcalendar;

import net.fortuna.ical4j.data.CalendarBuilder;
import net.fortuna.ical4j.data.CalendarOutputter;
import net.fortuna.ical4j.model.Calendar;
import net.fortuna.ical4j.model.Property;
import net.fortuna.ical4j.model.component.CalendarComponent;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.URL;
import java.util.Arrays;
import java.util.HashMap;

public class Main {
	public static void main(String[] args) throws Exception {
		String calendarUrl = args[0];
		InputStream is = new URL(calendarUrl).openStream();
		CalendarBuilder builder = new CalendarBuilder();
		Calendar calendar = builder.build(is);

		for (CalendarComponent calendarComponent : calendar.getComponents()) {
			for (Property property : calendarComponent.getProperties()) {
				if (property.getName().equals("DESCRIPTION")) {
					String[] descriptionTags = property.getValue().split("\n");

					HashMap<String, String> splitDescriptionTags = new HashMap<>();

					Arrays.stream(descriptionTags)
						  .forEach(tag -> {
							String[] split = tag.split(": ");
							splitDescriptionTags.put(split[0], split[1]);
						  });

					String nameOfLecture = splitDescriptionTags.get("Description");
					String typeOfLecture = splitDescriptionTags.get("Event type");

					if (nameOfLecture != null) {
						if (typeOfLecture != null) {
							calendarComponent.getProperty(Property.SUMMARY).setValue(nameOfLecture + " " + typeOfLecture);
						}
						else {
							calendarComponent.getProperty(Property.SUMMARY).setValue(nameOfLecture);
						}
					}
				}
			}
		}

		// FileOutputStream fout = new FileOutputStream("calendar-adjusted.ics");
		CalendarOutputter outputter = new CalendarOutputter(false);
		// outputter.output(calendar, fout);
		outputter.output(calendar, System.out);
	}
}
