const daysTag = document.querySelector(".days");
currentDate = document.querySelector(".current-date");
prevNextIcon = document.querySelectorAll(".icons span");

let date = new Date();
let currYear = date.getFullYear();
let currMonth = date.getMonth();

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

const renderCalendar = () => {
  let firstDayofMonth = new Date(currYear, currMonth, 1).getDay();
  let lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate();
  let lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay();
  let lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();
  let liTag = "";

  for (let i = firstDayofMonth; i > 0; i--) {
    liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
  }

  for (let i = 1; i <= lastDateofMonth; i++) {
    let isToday = i === date.getDate() && currMonth === new Date().getMonth() && currYear === new Date().getFullYear() ? "active" : "";

    if (i === date.getDate() && currMonth === new Date().getMonth() && currYear === new Date().getFullYear()) {
      liTag += `<li class="${isToday}">${i}</li>`;
    } else {
      let currentDate = new Date(currYear, currMonth, i);
      let today = new Date();
      if (currentDate < today) {
        liTag += `<li class="inactive">${i}</li>`;
      } else {
        liTag += `<li class="${isToday}">${i}</li>`;
      }
    }
  }

  for (let i = lastDayofMonth; i < 6; i++) {
    liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
  }
  currentDate.innerText = `${months[currMonth]} ${currYear}`;
  daysTag.innerHTML = liTag;
};

renderCalendar();

prevNextIcon.forEach(icon => {
  icon.addEventListener("click", () => {
    currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
    if (currMonth < 0 || currMonth > 11) {
      date = new Date(currYear, currMonth, new Date().getDate());
      currYear = date.getFullYear();
      currMonth = date.getMonth();
    } else {
      date = new Date();
    }
    renderCalendar();
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const checkboxes = document.querySelectorAll(".filter-checkbox");
  const radios = document.querySelectorAll(".filter-radio");

  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", applyFilters);
  });

  radios.forEach(function(radio) {
    radio.addEventListener("click", applyFilters);
  });

  function applyFilters() {
    const selectedCategories = getSelectedValues(".filter-checkbox");
    const selectedRating = getSelectedValue(".filter-radio");

    const items = document.querySelectorAll(".item");
    items.forEach(function(item) {
      const category = item.dataset.category;
      const rating = item.dataset.rating;

      if ((selectedCategories.length === 0 || selectedCategories.includes(category)) &&
          (selectedRating === "" || rating === selectedRating)) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  }

  function getSelectedValues(selector) {
    const selectedValues = [];
    const elements = document.querySelectorAll(selector);
    elements.forEach(function(element) {
      if (element.checked) {
        selectedValues.push(element.value);
      }
    });

    return selectedValues;
  }

  function getSelectedValue(selector) {
    const elements = document.querySelectorAll(selector);

    for (let i = 0; i < elements.length; i++) {
      if (elements[i].checked) {
        return elements[i].value;
      }
    }

    return "";
  }

  function getCalendarDate() {
    const calendarDates = document.querySelectorAll(".days li");
    calendarDates.forEach(function(date) {
      date.addEventListener("click", function() {
        let newDate = new Date();
        const selectedDate = parseInt(date.innerText);
        let selectedMonth = newDate.getMonth() + 1;
        const selectedYear = newDate.getFullYear();

        console.log(`Selected Date: ${selectedDate}`);
        console.log(`Selected Month: ${selectedMonth}`);
        console.log(`Selected Year: ${selectedYear}`);
      });
    });
  }

  getCalendarDate();
});
