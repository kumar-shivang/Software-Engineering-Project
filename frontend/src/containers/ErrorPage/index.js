import { useRouteError } from "react-router-dom";

export default function ErrorPage() {

  return (
    <div className="bg-gray-100 flex items-center justify-center min-h-screen">
        <div id="error-page" className="text-center p-6 bg-white shadow-md rounded-lg">
            <h1 className="text-4xl font-bold text-red-500 mb-4">Oops!</h1>
            <p className="text-lg text-gray-700">Sorry, an unexpected error has occurred.</p>
        </div>
    </div>
  );
}