# Clickatell AI Assistant - Structured Code Organization

## 📁 Project Structure

```
rad-gp-c25-p-i6/
├── app/                          # Main application
│   └── main.py                   # Streamlit app entry point
├── src/                          # Source code
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration settings
│   │   └── rag_engine.py         # RAG implementation
│   ├── ui/                       # User interface
│   │   ├── __init__.py
│   │   ├── components.py         # UI components
│   │   └── styles.py             # CSS styles
│   └── utils/                    # Utility functions
│       ├── __init__.py
│       └── helpers.py            # Helper functions
├── tests/                        # Test files
│   ├── __init__.py
│   └── test_core.py              # Core functionality tests
├── data/                         # Data files
│   └── knowledge_base_clickatell.txt
├── vector_store/                 # FAISS index
│   └── faiss_index/
├── config/                       # Legacy config (kept for compatibility)
│   └── settings.py
├── .env                          # Environment variables
├── requirements_streamlit.txt    # Dependencies
└── run_structured_app.py         # Application launcher
```

## 🚀 How to Run

### Quick Start
```bash
python run_structured_app.py
```

### Manual Start
```bash
streamlit run app/main.py
```

## 📦 Code Organization Benefits

### ✅ **Separation of Concerns**
- **Core**: Business logic and RAG engine
- **UI**: Streamlit components and styling
- **Utils**: Reusable helper functions
- **Tests**: Automated testing

### ✅ **Maintainability**
- Modular code structure
- Clear import paths
- Reusable components
- Centralized configuration

### ✅ **Scalability**
- Easy to add new features
- Simple to modify existing functionality
- Clear testing structure
- Professional organization

## 🔧 Key Components

### **Core Module** (`src/core/`)
- `config.py`: Centralized configuration
- `rag_engine.py`: RAG implementation with proper class structure

### **UI Module** (`src/ui/`)
- `components.py`: Reusable Streamlit components
- `styles.py`: CSS styling separated from logic

### **Utils Module** (`src/utils/`)
- `helpers.py`: Common utility functions
- Message hashing, validation, etc.

### **Tests** (`tests/`)
- `test_core.py`: Core functionality tests
- Ensures no recursion issues
- Validates helper functions

## 🎯 Features

- ✅ **No Recursion**: Proper state management
- ✅ **Modern UI**: Clean, professional design
- ✅ **Modular Code**: Well-organized structure
- ✅ **Tested**: Automated test suite
- ✅ **Configurable**: Centralized settings
- ✅ **Maintainable**: Clear separation of concerns

## 🧪 Testing

Run tests independently:
```bash
python tests/test_core.py
```

Tests verify:
- Message hashing works correctly
- Fallback detection functions properly
- Input validation prevents issues
- No recursion in message processing

## 🔄 Migration from Old Structure

The structured version maintains compatibility with existing data and configuration while providing better organization for future development.

Old files are preserved for reference, but the new structure should be used for all future development.