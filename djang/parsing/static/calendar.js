function getAttributes() {
    const fragment = window.location.hash.substr(1);
    const urlParams = new URLSearchParams(fragment);
    return urlParams;
}

function setAttributes(attr) {
    const hash = `${attr.toString()}`;
    window.location.hash = hash;
}

function setAttributeSingle(name, value) {
    const attr = getAttributes();
    attr.set(name, value);
    setAttributes(attr);
}

let sources = new Set();
const annotatedSources = {};

function selectColor(number) {
  const hue = number * 137.508; // use golden angle approximation
  return `hsl(${hue},50%,75%)`;
}

async function createLabels(calendarApi) {
    const calendar_list = document.getElementById('calendar-list');
    const request = new Request('/api/calendars/');
    const res = await fetch(request);
    const json_res = await res.json();
    const calendars = json_res.calendars;
    calendars.forEach(calendar => {

        annotatedSources[calendar.id] = calendar.title;

        const div = document.createElement("div");
        div.setAttribute("x-name", calendar.title);
        div.setAttribute("x-id", calendar.id);
        div.className = "list-group-item list-group-item-action list-group-item-light p-3";
        calendar_list.appendChild(div);

        const inputId = `check-${calendar.id}`;
        const input = document.createElement("input");
        input.className = "form-check-input";
        input.type = "checkbox";
        input.id = inputId;
        input.checked = sources.has(calendar.id) ? 'checked' : '';

        const onChange = (t) => {
            if (t.checked) {
                sources.add(calendar.id);
                updateSourceAttributes();
                calendarApi.addEventSource({
                    id: calendar.id,
                    url: `/api/events/${calendar.id}`,
                    color: selectColor(calendar.id),
                });
            } else {
                const eventSource = calendarApi.getEventSourceById(calendar.id);
                if (eventSource) {
                    sources.delete(calendar.id);
                    eventSource.remove();
                    updateSourceAttributes();
                }
            }
        };
        input.addEventListener('change', (event) => onChange(event.currentTarget));
        onChange(input);

        div.appendChild(input);

        const label = document.createElement("label");
        label.htmlFor = inputId;
        label.className = "flexCheckDefault";
        label.innerText = calendar.title;
        div.appendChild(label);
    });
}


function updateSourceAttributes() {
    if (sources) {
        setAttributeSingle("sources", Array.from(sources).join(","));
    }
}


let calendar;
document.addEventListener('DOMContentLoaded', async function() {
    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap5',
    });
    const attrs = getAttributes();
    const initialView = attrs.get('view') || 'dayGridMonth';
    changeView(initialView);
    const initialDate = attrs.get('date');
    if (initialDate) {
        const date = new Date(initialDate);
        calendar.gotoDate(date);
    }
    calendar.on('datesSet', (dateProfile, context) => {
        const date = new Date((dateProfile.start.getTime() + dateProfile.end.getTime()) / 2);
        // Get YYYY-MM-DD but in current timezone
        const dateString = date.toLocaleString('sv').slice(0, 10);
        setAttributeSingle('date', dateString);
    });

    // Sources
    sources = new Set((getAttributes().get('sources') || '').split(',').map(i => Number(i)));

    // Event Click
    calendar.on("eventClick", (info) => {
      info.jsEvent.preventDefault();

      const modal = new bootstrap.Modal(document.getElementById('myModal'), {
        keyboard: false
      });

      document.getElementById('modalTitle').innerText=info.event.title;
      const locationElement = document.getElementById('modalLocation')
      const location = info.event.location;
      if (location) {
        locationElement.innerText = location;
      } else {
        locationElement.innerHTML = '<i>unknown</i>'
      }
      const start = info.event.start; 
      document.getElementById('modalStart').innerText=`${start.toLocaleDateString()} ${start.toLocaleTimeString()}`;
      const end = info.event.end;
      document.getElementById('modalEnd').innerText=`${end.toLocaleDateString()} ${end.toLocaleTimeString()}`;

      
      document.getElementById('modalCalendar').innerText=annotatedSources[info.event.source.id];

      modal.show();
    });

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
    switch (view) {
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
