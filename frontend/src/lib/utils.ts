

export function getCookie(name: string) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}


export const defaultUnauthorizedHandler = () => {
    if (!window.location.pathname.startsWith('/login')) {
        const currentPath = window.location.pathname;
        const searchParams = new URLSearchParams();
        searchParams.set('next', currentPath);
        window.location.href = `/r/login?${searchParams.toString()}`;
    }
};