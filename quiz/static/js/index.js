tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
        colors: {
            primary: "#1173d4",
            "background-light": "#f6f7f8",
            "background-dark": "#101922",
            "content-light": "#111418",
            "content-dark": "#f6f7f8",
            "subtle-light": "#617589",
            "subtle-dark": "#a0b3c6",
            "border-light": "#dbe0e6",
            "border-dark": "#2c3e50",
        },
        fontFamily: {
            display: ["Inter", "sans-serif"],
        },
        borderRadius: {
            DEFAULT: "0.5rem",
            lg: "0.75rem",
            xl: "1rem",
            full: "9999px",
        },
        },
    },
};


// Disable buttons when they are clicked to avoid double clicking and overloading the server

const backDashboardBtn = document.querySelector('#back-dashboard-btn')

backDashboardBtn.addEventListener('click', function(e){
    e.preventDefault();

    backDashboardBtn.classList.remove('bg-primary');
    backDashboardBtn.classList.add('bg-gray-500');
    backDashboardBtn.classList.add('cursor-not-allowed');

});