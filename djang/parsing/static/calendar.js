async function createLabels(calendarApi) {
  const calendar_list = document.getElementById('calendar-list');
  const request = new Request('/api/calendars/');
  const res = await fetch(request);
  const json_res = await res.json();
  const calendars = json_res.calendars;
  calendars.forEach(calendar => {

    const div = document.createElement("div");
    //input.type="checkbox";
    div.setAttribute("x-name", calendar.title);
    div.className="list-group-item list-group-item-action list-group-item-light p-3";
    calendar_list.appendChild(div);

    const inputId = `check-${calendar.id}`;

    const input = document.createElement("input");
    input.className="form-check-input";
    input.type="checkbox";
    input.id = inputId;

    input.addEventListener('change', (event) => {
      if (event.currentTarget.checked) {
        calendarApi.addEventSource(
          {
            id: calendar.id,
            url: `/api/events/${calendar.id}`,
          },
        );
      } else {
        const eventSource = calendarApi.getEventSourceById(calendar.id);
        if (eventSource) {
          eventSource.remove();
        }
      }
    });

    div.appendChild(input);

    const label = document.createElement("label");
    label.htmlFor=inputId;
    label.className = "flexCheckDefault";
    label.innerText = calendar.title;
    div.appendChild(label);
  });
}

function getAttributes() {
  const fragment = window.location.hash.substr(1);
  const urlParams = new URLSearchParams(fragment);
  return urlParams;
}

function setAttributes(attr) {
  const hash = `${attr.toString()}`;
  window.location.hash = hash;
}

let calendar;
document.addEventListener('DOMContentLoaded', async function() {
  const calendarEl = document.getElementById('calendar');
  calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: 'bootstrap5',
  });
  const initialView = getAttributes().get('view') || 'dayGridMonth';
  changeView(initialView);
  calendar.render();

  await createLabels(calendar);
});

function filterCalendars(text) {
  const calendar_list = document.getElementById('calendar-list');
  calendar_list.childNodes.forEach(c => {
    if (!c.tagName) {
      return;
    }
    const xname = c.getAttribute("x-name");
    c.style.display = (xname && xname.includes(text)) ? '' : 'none';
  });
}

function changeView(view) {
  switch(view) {
    case "month":
      calendar.changeView('dayGridMonth');
      break;
    case "week":
      calendar.changeView('dayGridWeek');
      break;
    case "day": 
      calendar.changeView('timeGridDay');
      break;
  }
  const attr = getAttributes();
  attr.set('view', view);
  setAttributes(attr);
}
