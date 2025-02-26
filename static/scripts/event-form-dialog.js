import { initDialog } from "./dialog.js";
import { initEventForm } from "./event-form.js";
import { initToaster } from "./toaster.js";

export function initEventFormDialog() {
  const dialog = initDialog("event-form");
  const toaster = initToaster(dialog.dialogElement);
  const eventForm = initEventForm(toaster);

  const dialogTitleElement = dialog.dialogElement.querySelector("[data-dialog-title]");

  document.addEventListener("event-create-request", (event) => {
    dialogTitleElement.textContent = "Create event";
    eventForm.switchToCreateMode(
      event.detail.date,
      event.detail.startTime,
      event.detail.endTime
    );
    dialog.open();
  });

  document.addEventListener("event-edit-request", (event) => {
    dialogTitleElement.textContent = "Edit event";
    eventForm.switchToEditMode(event.detail.event);
    dialog.open();
  });

  dialog.dialogElement.addEventListener("close", () => {
    eventForm.reset();
  });

  eventForm.formElement.addEventListener("event-create", () => {
    dialog.close();
  });

  eventForm.formElement.addEventListener("event-edit", () => {
    dialog.close();
  });

  document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/schedules/")
        .then(response => response.json())
        .then(schedules => {
            console.log("Fetched schedules:", schedules); // Kiểm tra dữ liệu lấy về

            const eventTemplate = document.querySelector('template[data-template="event"]');
            const eventListItemTemplate = document.querySelector('template[data-template="event-list-item"]');

            // Kiểm tra nếu không tìm thấy template
            if (!eventTemplate || !eventListItemTemplate) {
                console.error("Không tìm thấy template sự kiện!");
                return;
            }

            const calendar = document.querySelector("[data-calendar]"); // Kiểm tra container chứa lịch
            if (!calendar) {
                console.error("Không tìm thấy phần tử data-calendar!");
                return;
            }

            schedules.forEach(schedule => {
                // Clone phần tử danh sách sự kiện
                const eventListItem = eventListItemTemplate.content.cloneNode(true);
                const eventElement = eventTemplate.content.cloneNode(true);

                // Gán dữ liệu vào sự kiện
                eventElement.querySelector("[data-event-title]").textContent = `${schedule.class_assigned_name} (${schedule.teacher_name})`;
                eventElement.querySelector("[data-event-start-time]").textContent = schedule.start_time.substring(0, 5);
                eventElement.querySelector("[data-event-end-time]").textContent = schedule.end_time.substring(0, 5);

                // Chèn sự kiện vào trong danh sách sự kiện
                eventListItem.querySelector("[data-event-list-item]").appendChild(eventElement);

                // Chèn danh sách sự kiện vào lịch
                calendar.appendChild(eventListItem);
            });
        })
        .catch(error => console.error("Lỗi khi lấy dữ liệu lịch:", error));
});



}