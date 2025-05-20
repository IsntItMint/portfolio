TARGET = etch2D

BUILD_DIR := ./build

SRC_DIR := ./src

SRCS = $(shell find $(SRC_DIR) -name '*.cpp') 

OBJS = $(SRCS:%=$(BUILD_DIR)/%.o)

DEPS := $(OBJS:.o=.d)

INC_DIRS := $(shell find $(SRC_DIR) -type d) $(HOME)/.local/include ./include

INC_FLAGS := $(addprefix -I, $(INC_DIRS))

CPPFLAGS := $(INC_FLAGS) -MMD -MP

CFLAGS := -march=native -O3 -DNDEBUG -std=c++17 -Wall -fopenmp

LIB_DIRS :=

LIB_FLAGS := -fopenmp

$(BUILD_DIR)/$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $@ $(LIB_DIRS) $(LIB_FLAGS)

$(BUILD_DIR)/%.cpp.o: %.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

.PHONY: clean
figclean:
	-rm -r fig/simulation/*
dataclean: figclean
	-rm -r data/simulation/*
clean: dataclean
	-rm -r $(BUILD_DIR)/*
