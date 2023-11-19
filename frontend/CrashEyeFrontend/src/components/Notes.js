import React, { useEffect, useState } from 'react';
import Modal from 'react-modal'; // Import react-modal
const Notes = () => {
  // Sample data for the clickable blocks
  const [criticalError, setCriticalError] = useState([]);
  const [fatalError, setFatalError] = useState([]);
  const [warningError, setWarningError] = useState([]);
  const [ischecked, setIsChecked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isConfirmationModalOpen, setIsConfirmationModalOpen] = useState(false);
  async function getWarningError() {
    const response = await fetch("https://crasheyeapi.onrender.com/api/getWarningCrash/");
    if (response) {
      setWarningError(await response.json());
    }
  }
  async function getCriticalError() {
    const response = await fetch("https://crasheyeapi.onrender.com/api/getCriticalCrash/");
    if (response) {
      setCriticalError(await response.json());
    }
  }
  async function getFatalError() {
    const response = await fetch("https://crasheyeapi.onrender.com/api/getFatalCrash/");
    if (response) {
      setFatalError(await response.json());
    }
  }
  const openConfirmationModal = () => {
    setIsConfirmationModalOpen(true);
  };
  const closeConfirmationModal = () => {
    setIsConfirmationModalOpen(false);
  };

  useEffect(() => {
    getWarningError();

    getFatalError();

    getCriticalError();
  }, []);

  let blocks = criticalError.concat(fatalError, warningError);

  // State to manage the selected block
  const [selectedBlock, setSelectedBlock] = useState(null);

  // State to manage the selected error class
  const [selectedErrorClass, setSelectedErrorClass] = useState("CRITICAL");

  // Function to handle block selection
  const handleBlockClick = (block) => {
    setSelectedBlock(block);
  };

  // Function to handle error class selection
  const handleClassClick = (errorClass) => {
    setSelectedErrorClass(errorClass);
  };
  const removeData = async (blockToSend) => {
    console.log(blockToSend);
    const classToUpdate = blockToSend.Class;
    fetch('https://crasheyeapi.onrender.com/deleteCrash/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(blockToSend)
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Failed to delete the crash');
        }
      })
      .then((data) => {
        // Handle the response from the server
        // You can update the state or perform any other actions here
        console.log(data);
      })
      .catch((error) => {
        // Handle any errors that occur during the request
        console.error(error);
      });
    if (classToUpdate === "CRITICAL") {
      await getCriticalError();
    }
    if (classToUpdate === "WARNING") {
      await getWarningError();
    }
    if (classToUpdate === "FATAL") {
      await getFatalError();
    }
    blocks = criticalError.concat(fatalError, warningError);
  }
  const handleCheckBox = () => {
    setIsChecked(true);
    const blockToSend = selectedBlock;
    setLoading(true)
    setTimeout(() => {
      setIsChecked(false);
      setLoading(false);
      setSelectedBlock(null);
    }, 10000);
    removeData(blockToSend);
  }
  const handleCheckboxConfirmation = () => {
    closeConfirmationModal(); // Close the confirmation modal
    handleCheckBox(); // Proceed with your checkbox handling logic
  };

  return (

    <div className="flex h-fit bg-gray-900 text-white">
      {/* 30% width container */}
      {console.log("Initally checked", ischecked)}
      <div className="flex flex-col w-1/3 h-fit bg-gray-800 p-4 justify-start">
        <div className=' text-lg w-full'>
          <button
            className={`mb-2 p-2 w-1/3 cursor-pointer ${selectedErrorClass === 'FATAL' ? 'bg-blue-500' : 'bg-gray-700'
              }`}
            onClick={() => handleClassClick('FATAL')}
          >
            Fatal
          </button>
          <button
            className={`mb-2 p-2  w-1/3 cursor-pointer ${selectedErrorClass === 'CRITICAL' ? 'bg-blue-500' : 'bg-gray-700'
              }`}
            onClick={() => handleClassClick('CRITICAL')}
          >
            Critical
          </button>
          <button
            className={`mb-2 p-2 w-1/3 cursor-pointer ${selectedErrorClass === 'WARNING' ? 'bg-blue-500' : 'bg-gray-700'
              }`}
            onClick={() => handleClassClick('WARNING')}
          >
            Warning
          </button>
        </div>
        <div className="flex flex-col gap-9">
          <ul className='overflow-y-auto h-screen scrollbar-thin scrollbar-thumb-slate-200 scrollbar-track-zinc-800'>
            {blocks
              .filter((block) => !selectedErrorClass || block.Class === selectedErrorClass)
              .map((block) => (
                <li
                  key={block._id}
                  className="mb-2"
                  onClick={() => handleBlockClick(block)}
                  style={{ cursor: 'pointer' }}
                >
                  <div className="bg-gray-700 p-2 shadow hover:shadow-md">
                    <h2 className="text-lg font-semibold">{block.fname}</h2>
                    <p className="text-sm text-gray-300">{block.Class}</p>
                    <p className="text-xs text-gray-400">{block.tstamp}</p>
                  </div>
                </li>
              ))}
          </ul>
          <button className='w-1/3 fixed rounded-lg bottom-0 left-0 bg-green-600 text-2xl text-white font-bold py-5' onClick={() => window.location.reload()}>Refresh</button>
        </div>

      </div>

      {/* 70% width container */}
      <div className=" flex flex-col w-2/3 bg-gray-900 p-4 my-4">

        {selectedBlock && (
          <>
            <div className="flex items-start justify-start top-3 right-0 gap-5">
              <input id="green-checkbox" type="checkbox" value="" className=" w-8 h-8 rounded-xl accent-green-500" checked={ischecked} onChange={openConfirmationModal} />
              <p className='text-2xl text-center'>Resolved</p>
            </div>
            <div className='flex flex-col items-center'>

              <h1 className="text-2xl text-center font-semibold mb-4">{selectedBlock.fname}</h1>
              <p className="text-sm text-center text-gray-300 mb-5">{selectedBlock.tstamp}</p>
              <div className="flex flex-col items-start text-xl text-gray-300 mt-10">
                <p className=' text-center'>System: {selectedBlock.System}</p>
                <br></br>
                <p className=' text-center'>Version: {selectedBlock.Version}</p>
                <br></br>
                <p className=' text-center'>Machine: {selectedBlock.Machine}</p>
                <br></br>
                <p className=' text-center'>Processor: {selectedBlock.Processor}</p>
                <br></br>
                <p className=' text-center'>RAM Usage: {selectedBlock["RAM Usage"]}</p>

              </div>
              {loading && (
                <p className='w-full bg-orange-600 py-10 text-center text-2xl mt-6'>Loading...</p>
              )}
            </div>
            <Modal
              isOpen={isConfirmationModalOpen}
              contentLabel="Confirm Checkbox"
              onRequestClose={closeConfirmationModal}
              className="modal" // Apply a custom class for the modal container
            >
              <h2 className="text-2xl mb-4 text-center">Confirm Checkbox</h2>
              <p className="text-gray-700 mb-4 text-center">Are you sure you want to proceed?</p>
              <div className='flex items-center justify-center'>
                <button
                  className="bg-green-500 text-white py-2 px-4 rounded mr-4"
                  onClick={handleCheckboxConfirmation}
                >
                  Confirm
                </button>
                <button
                  className="bg-red-500 text-white py-2 px-4 rounded"
                  onClick={closeConfirmationModal}
                >
                  Cancel
                </button>
              </div>
            </Modal>

          </>


        )}

      </div>
    </div>
  );
};

export default Notes;
