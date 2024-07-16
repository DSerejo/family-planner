export async function fetchData() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ data: "Dummy data" });
      }, 1000);
    });
  }